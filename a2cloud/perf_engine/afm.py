#!/usr/bin/env python

"""
a2cloud application feature measurement tool

Utilizes Linux Performance Tools (perf) for measuring application vector components.
"""

import argparse
import csv
import json
from StringIO import StringIO
import subprocess
import sys
import time
import uuid
from counters import CacheCounters, FPCounters, MemCounters
from vectors import AppVector

def main():
    """
    Main function. Handles argument parsing.
    """
    parser = MyParser(prog='afm',
                      description='a2cloud script for measuring application vector components',
                      epilog='email questions to Cody Balos <r_balos@u.pacific.edu>')
    subparsers = parser.add_subparsers(help='tools', dest='tool')

    measure_parser = subparsers.add_parser('measure', description='measure application features')
    measure_parser.add_argument('appname', help='name of the application to be profiled')
    measure_parser.add_argument('cmd', help='application command to execute')

    report_parser = subparsers.add_parser('report', description='read result JSON file output by measure command')
    report_parser.add_argument('files', nargs='+', help='result JSON file(s)')
    report_parser.add_argument('-s', '--sort',
        default='arithmetic_intensity',
        help='app vector component to sort report by (e.g. -s spflops)')

    args, unknown = parser.parse_known_args()
    if args.tool == 'measure':
        counters = [
            FPCounters.fp_comp_ops_exe__sse_x87,
            FPCounters.fp_comp_ops_exe__sse_packed_double,
            FPCounters.fp_comp_ops_exe__sse_packed_single,
            FPCounters.fp_comp_ops_exe__sse_scalar_double,
            FPCounters.fp_comp_ops_exe__sse_scalar_single,
            FPCounters.simd_fp_256__packed_double,
            FPCounters.simd_fp_256__packed_single,
            CacheCounters.llc_load_misses,
            CacheCounters.llc_stores,
            CacheCounters.llc_loads,
            CacheCounters.llc_stores,
            MemCounters.uncore_imc_0__cas_count_read,
            MemCounters.uncore_imc_1__cas_count_read,
            MemCounters.uncore_imc_2__cas_count_read,
            MemCounters.uncore_imc_3__cas_count_read,
            MemCounters.uncore_imc_4__cas_count_read,
            MemCounters.uncore_imc_5__cas_count_read,
            MemCounters.uncore_imc_6__cas_count_read,
            MemCounters.uncore_imc_7__cas_count_read,
            MemCounters.uncore_imc_0__cas_count_write,
            MemCounters.uncore_imc_1__cas_count_write,
            MemCounters.uncore_imc_2__cas_count_write,
            MemCounters.uncore_imc_3__cas_count_write,
            MemCounters.uncore_imc_4__cas_count_write,
            MemCounters.uncore_imc_5__cas_count_write,
            MemCounters.uncore_imc_6__cas_count_write,
            MemCounters.uncore_imc_7__cas_count_write,
        ]
        session = Session(counters=counters, appname=args.appname, cmd=args.cmd, cmdflags=unknown)
        session.measure(iterations=10)
        filename = '%s_afm_results.json' % session.date
        with open('%s_afm_results.json' % session.date, 'w') as f:
            f.write(json.dumps(session.to_dict()))
            print((ANSI.OKBLUE + 'results saved to %s' + ANSI.ENDC) % filename)
    else:
        apps = [(f, AppVector.from_afm_json_file(f)) for f in args.files]
        apps.sort(key=lambda x: getattr(x[1], args.sort), reverse=True)
        for app in apps:
            print('===========================================================')
            print(app[0])
            print(vars(app[1]))
            print('arithmetic intensity = %0.4f' % app[1].arithmetic_intensity)


class Session:
    """Represents a measurement session.
    """
    def __init__(self, counters, appname, cmd, cmdflags):
        self.id = uuid.uuid1()
        self.date = time.strftime("%Y%m%d_%H%M%S")
        self.oskernel = get_kernel()
        self.hardware = get_hardware()
        self.counters = counters
        self.appname = appname
        self.cmd = cmd
        self.cmdflags = cmdflags
        self.results = None
        print(ANSI.BOLD + ('Session ID: %s\n' % str(self.id)) + ANSI.ENDC)
        #print('OS Kernel: %s' % self.oskernel)
        #print('Hardware Information:\n%s' % self.hardware)


    def measure(self, iterations=1):
        """Run `perf stat` to measure counters we are interested in.
        """
        perf_cmd = ['perf', 'stat', '-x', ',', '-A', '-C0,47', '-e']
        perf_cmd.append(','.join(self.counters))
        # ensure all memory is allocated on single chip so we get consistent numbers
        perf_cmd.extend(['numactl', '--membind=0', '--physcpubind=0'])
        perf_cmd.append(self.cmd)
        perf_cmd.extend(self.cmdflags)
        print(ANSI.BOLD + 'Running command:' + ANSI.ENDC)
        print(' '.join(perf_cmd))
        print('')
        outputs = []
        for i in range(iterations):
            perf_proc = subprocess.Popen(perf_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outs, errs = perf_proc.communicate()
            if perf_proc.returncode != 0:
                print(ANSI.FAIL + "perf returned an error:")
                print(errs + ANSI.ENDC)
                sys.exit(-1)
            else:
                # for some reason output is going to errs instead of outs
                outputs.append(errs)
        try:
            self.results = parse_perf_output(''.join(outputs))
        except:
            print(ANSI.BOLD + ANSI.FAIL + 'Failed to parse perf output:' + ANSI.ENDC + ANSI.FAIL)
            print(outputs)
            sys.exit(-1)
            print(ANSI.BOLD + ANSI.OKGREEN + 'Done!' + ANSI.ENDC)
            return self.results


    def to_dict(self):
        """Returns dict representing the Session object
        """
        d = {}
        d['session_id'] = str(self.id)
        d['timestamp'] = self.date
        d['oskernel'] = self.oskernel
        d['hardware'] = self.hardware
        d['counters'] = ','.join(self.counters)
        d['appname'] = self.appname
        d['cmd'] = self.cmd
        d['cmdflags'] = self.cmdflags
        d['results'] = self.results
        return d


def parse_perf_output(output):
    """Parses output from perf.

    Output should be a comma delimited string.
    """
    stats = {}
    reader = csv.reader(StringIO(output))
    for row in reader:
        key = row[0] + '/' + row[3]
        val = row[1]
        if key not in stats:
            stats[key] = [val]
        else:
            stats[key].append(val)
    return stats


def get_kernel():
    """Returns current kernel version.
    """
    return subprocess.check_output(['uname', '-r'])


def get_hardware():
    """Returns current hardware information.
    """
    return subprocess.check_output(['lscpu'])


class ANSI():
    """ANSI color escape sequences.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MyParser(argparse.ArgumentParser):
    """ Custom argparse.ArgumentParser which prints help if program arguments are used improperly.
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == "__main__":
    sys.exit(main())

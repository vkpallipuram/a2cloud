"""Arithmetic intensity and app vector components based on afm results.
"""

import json
import numpy as np
from counters import CacheCounters, FPCounters, MemCounters


class AppVector():
    """ Application Vector. Default units are Mega.
    """

    def __init__(self):
        self.x87 = 0.0
        self.spflops = 0.0
        self.dpflops = 0.0
        self.memory = 0.0

    @property
    def arithmetic_intensity(self):
        """Get the arithmetic intensity of the application.
        """
        return np.log((self.x87 + self.spflops + self.dpflops)/self.memory)


    @staticmethod
    def from_afm_json_file(filename):
        afm = None
        stats = None

        with open(filename, 'r') as f:
            afm = json.load(f)
            stats = afm['results']

        cpu_flops_x87 = stats['CPU0/' + FPCounters.fp_comp_ops_exe__sse_x87]
        cpu_flops_scalar_single = stats['CPU0/' + FPCounters.fp_comp_ops_exe__sse_scalar_single]
        cpu_flops_scalar_double = stats['CPU0/' + FPCounters.fp_comp_ops_exe__sse_scalar_double]
        cpu_flops_packed_single = stats['CPU0/' + FPCounters.fp_comp_ops_exe__sse_packed_single]
        cpu_flops_packed_double = stats['CPU0/' + FPCounters.fp_comp_ops_exe__sse_packed_double]
        cpu_flops_256_packed_double = stats['CPU0/' + FPCounters.simd_fp_256__packed_double]
        cpu_flops_256_packed_single = stats['CPU0/' + FPCounters.simd_fp_256__packed_single]
        cpu_uncore_reads = dict_reduce(dict_filter(stats, ['CPU0', 'uncore_imc', 'read']))
        cpu_uncore_writes = dict_reduce(dict_filter(stats, ['CPU0', 'uncore_imc', 'write']))

        vector = AppVector()
        vector.x87 = np.mean([float(x) for x in cpu_flops_x87])*1.0E-6
        vector.spflops = (np.mean([float(x) for x in cpu_flops_scalar_single]) \
                            + np.mean([float(x) for x in cpu_flops_packed_single])*4 \
			    + np.mean([float(x) for x in cpu_flops_256_packed_single])*8)*1.0E-6
        vector.dpflops = (np.mean([float(x) for x in cpu_flops_scalar_double]) \
                            + np.mean([float(x) for x in cpu_flops_packed_double])*2 \
			    + np.mean([float(x) for x in cpu_flops_256_packed_double])*4)*1.0E-6
        vector.memory = np.mean([float(x) for x in cpu_uncore_reads]) \
                            + np.mean([float(x) for x in cpu_uncore_writes])

        return vector


def dict_reduce(d):
    val = []
    for i in range(10):
        count = 0.0
        for k in d:
            count += float(d[k][i])
        val.append(count)
    return val


def dict_filter(d, filters):
    return {k:v for k,v in d.items() if all(x in k for x in filters)}

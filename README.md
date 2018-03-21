# A2Cloud

A framework for empowering scientific and high-performance computing via the cloud.

[![Supports](https://img.shields.io/badge/python-2.7%2C%203.3%2C%203.4%2C%203.5%2C%203.6%2C%203.7--dev-blue.svg)](https://img.shields.io/badge/python-2.7%2C%203.3%2C%203.4%2C%203.5%2C%203.6%2C%203.7--dev-blue.svg)

## Setup and Dependencies

To get started, simply clone this repository

```
$ git clone https://github.com/cojomojo/a2cloud.git
```

To utilize the PERF engine (to extract application features), you must:

* Have [Linux perf tools](https://perf.wiki.kernel.org/index.php/Main_Page) installed
* Have a supported version of [Python](https://www.python.org/) installed
* Be on an x86_64 architecture (for now)

To utilize the cloud trace engine (to extract cloud instance features), you must:

* Have gfortran installed
* Have superuser privileges on the instance in question

## How to Use

To generate a application feature vector, utilize the PERF engine. The PERF engine can be used to extract features of your application on any x86_64 machine, it does not have to be done on the target cloud instances.

To generate a cloud feature vector, utilize the Cloud Trace Engine. This should be done on the cloud instance(s) you are interested in.

### The PERF Engine

One way to use the engine is to measure the features of your application:

```
$ cd a2cloud/perf_engine
$ ./afm.py measure MY_APP ~/codes/my_app arg1 arg2 argN
```

This will output a JSON file with the raw information. To view this information in a friendly way you can use the PERF engine's report feature:

```
$ ./afm.py report MY_APP_03122018.json
```

### The Cloud Trace Engine

To use this engine to measure the features of a cloud instance:

```
$ cd a2clooud/cloud_trace_engine
$ make
$ ./a2cloud-bench.sh # requires superuser
```

## Data Available

The `data` folder contains application and cloud vectors which have been collected so far. Application vectors can be explored easily using the PERF engine report feature:

```
$ ./afm.py report a2cloud/data/vectors/applications/**/*.json
===========================================================
../../data/vectors/applications/LULESH/LULESH_10.json
{'spflops': 0.0, 'x87': 16.891292899999996, 'dpflops': 594.24763610000002, 'memory': 40.768000000000001}
arithmetic intensity = 2.7074
===========================================================
../../data/vectors/applications/LULESH/LULESH_30.json
{'spflops': 0.0, 'x87': 3133.6285904000001, 'dpflops': 74272.050185100001, 'memory': 5246.4879999999994}
arithmetic intensity = 2.6915
.
.
.
```

## Read The Paper

The A2Cloud paper is currently under review in IEEE CLOUD 2018.

## Contributors

### University of the Pacific School of Engineering and Computer Science:

* [Cody Balos](https://github.com/cojomojo)
* Vivek Pallipuram, Ph.D (primary contact) - vpallipuramkrishnamani@pacific.edu
* Zachariah Abuelhaj
* David De La Vega
* David Mueller, Ph.D
* Chadi El Kari, Ph.D

## License

MIT

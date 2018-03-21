# linpack Fortran Benchmarks

*linpacks* runs the linpack single-precision benchmark with a 1000 x 1000 sized matrix.
*linpackd* runs the linpack double-precision benchmark with a 1000 x 1000 sized matrix.

Benchmarks are located at the following links:
[linpacks Fortran Benchmark](http://www.netlib.org/benchmark/1000s)
[linpackd Fortran Benchmark](http://www.netlib.org/benchmark/1000d)

## Building program
Build the programs with the included *Makefile*.

```
make: makes linpacks linpacks_x87 and linpackd and linpackd_x87 benchmarks.
make clean : removes the .o and .exe files

```

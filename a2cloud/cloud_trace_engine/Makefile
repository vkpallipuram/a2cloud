BENCH_DIR = $(shell lastname $(MAKEFILE_LIST))

all: linpack stream

linpack:
	$(MAKE) -C LINPACK

stream:
	$(MAKE) -C STREAM

clean:
	$(MAKE) clean -C LINPACK
	$(MAKE) clean -C STREAM

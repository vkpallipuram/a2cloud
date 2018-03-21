CC = gcc
CFLAGS = -O3

DEFINES = -DSTREAM_ARRAY_SIZE=20000000

all: stream_c.exe

stream_c.exe: stream.c
	$(CC) $(CFLAGS) $(DEFINES) stream.c -o stream_c.exe

clean:
	rm -f stream_c.exe *.o


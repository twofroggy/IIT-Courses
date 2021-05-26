CC=gcc
CFLAGS=-Wall -O3

build: matrixadd runtime

test-matrixadd: matrixadd
	./matrixadd 10000

test-runtime: runtime
	./runtime 10 1000 1

matrixadd: matrixadd.c
	$(CC) $(CFLAGS) -o matrixadd $<

runtime: runtime.c
	$(CC) $(CFLAGS) -o runtime $<

clean:
	rm -rf matrixadd runtime


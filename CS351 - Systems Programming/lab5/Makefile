CC=gcc
CFLAGS=-Wall -0fast -pthread

build: cpubench

test-cpubench: cpubench
	./runbench.sh

cpubench: cpubench.c
	$(CC) $(CFLAGS) -o cpubench $<

clean:
	rm -rf cpubench


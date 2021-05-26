CC=gcc
CFLAGS=-Wall -O3 -w 

build: netio socket-server

test-netio: test-netio.sh netio socket-server
	./test-netio.sh

netio: netio.c functions.o functions.h pipe-server.o
	$(CC) $(CFLAGS) -o $@ $^

pipe-server: % : %.c %.h
	$(CC) $(CFLAGS) -c $^

functions: % : %.c %.h
	$(CC) $(CFLAGS) -c $^

socket-server: % : %.c %.h functions.o
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -rf netio socket-server *.o *.out

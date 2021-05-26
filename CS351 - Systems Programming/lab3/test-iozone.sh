#!/bin/bash

# iterate over the program parameters using nested for loops
# program usage: ./fileio <workload> <block_size> <num_procs>
#     - workload: WS (write-sequential), WR (write-random), RS (read sequential), RR (read random)
#     - block_size: 64KB, 1MB, 64MB
#     - num_procs: 1 2 4 8 

# right now the bash script calls the program with only one configuration
workload=(WS WR RS RR)
block_size=(64 1024 16384)
num_procs=(1 2 4 8)


#4MB tests for latency 
for p in ${num_procs[@]}; do 
    /home/tiffany/iozone3_490/src/current/iozone -s 4m -r 4k -i 0 -i 1 -i 2 -t ${p} -O
done 

#1GB tests for throughput
for p in ${num_procs[@]}; do
    for b in ${block_size[@]}; do
        /home/tiffany/iozone3_490/src/current/iozone -s 1g -r ${b} -i 0 -i 1 -i 2 -t ${p}
  done
done

#Exiting the program
exit 0


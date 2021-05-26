#!/bin/bash

# iterate over the program parameters using nested for loops
# program usage: ./fileio <workload> <block_size> <num_procs>
#     - workload: WS (write-sequential), WR (write-random), RS (read sequential), RR (read random)
#     - block_size: 4KB, 64KB, 1MB, 64MB
#     - num_procs: 1 2 4 8

<<<<<<< HEAD
workload = (WS WR RS RR)
block_size = (4MB 2MB 1MB 500KB)
num_procs = (1 2 4 8)

# right now the bash script calls the program with only one configuration
./fileio $workload $block_size $num_procs
=======
workload=(WS WR RS RR)
block_size=(64KB 1MB 16MB)
num_procs=(1 2 4 8)

# right now the bash script calls the program with only one configuration
# ./fileio $workload $block_size $num_procs
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

#to create a 4 Mb file (binary way) (in bash script!!)
#for ((i = 0 ; i < $num_procs ; i++)); do
#    dd if=/dev/zero of=file$i.txt count=2048 bs=2048;
#done
<<<<<<< HEAD

#creating the 4MB datasets for latency
#D1
fallocate -x -l 4M file4mb
#D2
fallocate -x -l 2M file2mb-0
fallocate -x -l 2M file2mb-1
#D3
fallocate -x -l 1M file1mb-0
fallocate -x -l 1M file1mb-1
fallocate -x -l 1M file1mb-2
fallocate -x -l 1M file1mb-3
#D4
fallocate -x -l 500K file500kb-0
fallocate -x -l 500K file500kb-1
fallocate -x -l 500K file500kb-2
fallocate -x -l 500K file500kb-3
fallocate -x -l 500K file500kb-4
fallocate -x -l 500K file500kb-5
fallocate -x -l 500K file500kb-6
fallocate -x -l 500K file500kb-7

#creating the 1GB datasets for throughput
#D5
fallocate -x -l 1G file1gb
#D6
fallocate -x -l 500M file500-0
fallocate -x -l 500M file500-1
#D7
fallocate -x -l 250M file250-0
fallocate -x -l 250M file250-1
fallocate -x -l 250M file250-2
fallocate -x -l 250M file250-3
#D8
fallocate -x -l 125M file125-0
fallocate -x -l 125M file125-1
fallocate -x -l 125M file125-2
fallocate -x -l 125M file125-3
fallocate -x -l 125M file125-4
fallocate -x -l 125M file125-5
fallocate -x -l 125M file125-6
fallocate -x -l 125M file125-7
=======
#can't figure out hwo to do it with dd? it doesnt work with my fileio.c file 

#creating the 4MB datasets for latency
#D1
fallocate -x -l 4M file_lat_1proc
#D2
fallocate -x -l 2M file_lat_2procs0
fallocate -x -l 2M file_lat_2procs1
#D3
fallocate -x -l 1M file_lat_4procs0
fallocate -x -l 1M file_lat_4procs1
fallocate -x -l 1M file_lat_4procs2
fallocate -x -l 1M file_lat_4procs3
#D4
fallocate -x -l 500K file_lat_8procs0
fallocate -x -l 500K file_lat_8procs1
fallocate -x -l 500K file_lat_8procs2
fallocate -x -l 500K file_lat_8procs3
fallocate -x -l 500K file_lat_8procs4
fallocate -x -l 500K file_lat_8procs5
fallocate -x -l 500K file_lat_8procs6
fallocate -x -l 500K file_lat_8procs7

#creating the 1GB datasets for throughput
#D5
fallocate -x -l 1G file_tp_1proc
#D6
fallocate -x -l 500M file_tp_2procs0
fallocate -x -l 500M file_tp_2procs1
#D7
fallocate -x -l 250M file_tp_4procs0
fallocate -x -l 250M file_tp_4procs1
fallocate -x -l 250M file_tp_4procs2
fallocate -x -l 250M file_tp_4procs3
#D8
fallocate -x -l 125M file_tp_8procs0
fallocate -x -l 125M file_tp_8procs1
fallocate -x -l 125M file_tp_8procs2
fallocate -x -l 125M file_tp_8procs3
fallocate -x -l 125M file_tp_8procs4
fallocate -x -l 125M file_tp_8procs5
fallocate -x -l 125M file_tp_8procs6
fallocate -x -l 125M file_tp_8procs7
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

#to create a 1 Gb file (binary way)
#for ((i = 0 ; i < $num_procs ; i++)); do
#    dd if=/dev/zero of=file$i.txt count=1024 bs=1048576;
#done

#running all the configurations for 1GB throughput test 
for w in ${workload[@]}; do 
<<<<<<< HEAD
    for b in ${block_size[@]}; do 
=======
   for b in ${block_size[@]}; do 
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
        for p in ${num_procs[@]}; do 
            ./fileio ${w} ${b} ${p}
        done
    done
done

<<<<<<< HEAD
#set new array for the workloads only for throughput benchmarks
workload_latency = (WR RR)

#running all the configurations for 4MB latency test 
for w in ${workload_latency[@]}; do
    for n in ${num_procs[@]}; do
        ./fileio ${w} 4KB ${n} -O
=======
#set new array for the workloads only for latency benchmarks
workload_latency=(WR RR)

#running all the configurations for 4MB latency test 
for w in ${workload_latency[@]}; do
    for p in ${num_procs[@]}; do
        ./fileio ${w} 4KB ${p} -O
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
    done
done

#D1
<<<<<<< HEAD
rm file4mb

#D2
rm file2mb-0
rm file2mb-1

#D3
rm file1mb-0
rm file1mb-1
rm file1mb-2
rm file1mb-3

#D4
rm file500kb-0
rm file500kb-1
rm file500kb-2
rm file500kb-3
rm file500kb-4
rm file500kb-5
rm file500kb-6
rm file500kb-7

#D5
rm file1gb

#D6
rm file500-0
rm file500-1

#D7
rm file250-0
rm file250-1
rm file250-2
rm file250-3

#D8
rm file125-0
rm file125-1
rm file125-2
rm file125-3
rm file125-4
rm file125-5
rm file125-6
rm file125-7
=======
rm file_lat_1proc

#D2
rm file_lat_2procs0
rm file_lat_2procs1

#D3
rm file_lat_4procs0
rm file_lat_4procs1
rm file_lat_4procs2
rm file_lat_4procs3

#D4
rm file_lat_8procs0
rm file_lat_8procs1
rm file_lat_8procs2
rm file_lat_8procs3
rm file_lat_8procs4
rm file_lat_8procs5
rm file_lat_8procs6
rm file_lat_8procs7

#D5
rm file_tp_1proc

#D6
rm file_tp_2procs0
rm file_tp_2procs1

#D7
rm file_tp_4procs0
rm file_tp_4procs1
rm file_tp_4procs2
rm file_tp_4procs3

#D8
rm file_tp_8procs0
rm file_tp_8procs1
rm file_tp_8procs2
rm file_tp_8procs3
rm file_tp_8procs4
rm file_tp_8procs5
rm file_tp_8procs6
rm file_tp_8procs7
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

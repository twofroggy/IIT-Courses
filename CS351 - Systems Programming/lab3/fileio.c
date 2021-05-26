#define _GNU_SOURCE
#include <stdlib.h>
#include <fcntl.h>
#include <sys/time.h>
#include <stdio.h>
#include <unistd.h>
#include <wait.h>
#include <errno.h>
#include <string.h>

#define MSG "* running fileio %s workload with %s blocks and %s process(es)\n"

#define USAGE "usage: ./fileio <workload> <block_size> <num_procs> \n" \
"     - workload: WS / WR / RS / RR \n" \
"     - block_size: 4KB / 64KB / 1MB / 16MB \n" \
"     - num_procs: 1 / 2 / 4 / 8 \n" \
"     - WS = write-sequential \n" \
"     - WR = write-random \n" \
"     - RS = read-sequential \n" \
<<<<<<< HEAD
"     - RR = read-random \n" \

int main(int argc, char **argv)
{
    if (argc != 4) {
=======
"     - RR = read-random \n"

int main(int argc, char **argv)
{
    if (argc < 4) {
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
        printf(USAGE);
        exit(1);
    } else {
        printf(MSG, argv[1], argv[2], argv[3]);
    }

    //creating the variables
<<<<<<< HEAD
    int fp, i, upper, block_size, filesize, num_procs, num_ops, status;
=======
    int i, block_size, filesize, num_procs;
    int num_ops;
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
    ssize_t bytes_read = 0;
    struct timeval start, end;
    pid_t pid;
    const char *files[8];
<<<<<<< HEAD
    double time, opsPerSec, MBperS;
=======
    int limit;
    int status;
    int fp;
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

    //depending on given block size, set block_size accordingly
    if(strcmp(argv[2], "4KB") == 0){
        block_size = 4096;
    } else if(strcmp(argv[2], "64KB") == 0) {
        block_size = 65536;
    } else if(strcmp(argv[2], "1MB") == 0) {
        block_size = 1048576;
<<<<<<< HEAD
    } else if(strcmp(argv[2], "64MB") == 0) {
=======
    } else if(strcmp(argv[2], "16MB") == 0) {
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
        block_size = 67108864;
    }
    //error msg for when an invalid block size entered
    else{
        printf(USAGE);
        exit(1);
    }

    //(throughput - 1gb set (D5-D8), latency - 4mb set (D1-D4))
    // in the bashscripts, created mbfile.txt for 4mb n gbfile.txt for 1gb

<<<<<<< HEAD
    //if its for throughput for OPs/sec, name the appropriate amount of files
    if (argc == 5 && strcmp(argv[4], "-O") == 0) {
        if (strcmp(argv[3], "1") == 0){
            num_procs = 1;

            files[0] = "file4mb";

            filesize = 4194304;
        } else if (strcmp(argv[3], "2") == 0) {
            num_procs = 2;

            files[0] = "file2mb-0";
            files[1] = "file2mb-1";

            filesize = 2097152;
        } else if (strcmp(argv[3], "4") == 0) {
            num_procs = 4;

            files[0] = "file1mb-0";
            files[1] = "file1mb-1";
            files[2] = "file1mb-2";
            files[3] = "file1mb-3";

            filesize = 1048576;
      } else if (strcmp(argv[3],"8")==0){
            num_procs = 8;

            files[0] = "file500kb-0";
            files[1] = "file500kb-1";
            files[2] = "file500kb-2";
            files[3] = "file500kb-3";
            files[4] = "file500kb-4";
            files[5] = "file500kb-5";
            files[6] = "file500kb-6";
            files[7] = "file500kb-7";

            filesize = 512000;
      }
    }
    //if its for latency for MBs/sec, name the appropriate amount of files
=======
    //if its for latency for OPs/sec, name the appropriate amount of files
    if (argc == 5 && (strcmp(argv[4], "-O") == 0)) {
        if (strcmp(argv[3], "1") == 0){
            num_procs = 1;

            files[0] = "file_lat_1proc";

            filesize = 4194304;
        } else if (strcmp(argv[3], "2") == 0) { 
            num_procs = 2;

            files[0] = "file_lat_2procs0";
            files[1] = "file_lat_2procs1";

            filesize = 4194304 / 2;
        } else if (strcmp(argv[3], "4") == 0) { 
            num_procs = 4;

            files[0] = "file_lat_4procs0";
            files[1] = "file_lat_4procs1";
            files[2] = "file_lat_4procs2";
            files[3] = "file_lat_4procs3";

            filesize = 4194304 / 4;
      } else if (strcmp(argv[3], "8") == 0) { 
            num_procs = 8;

            files[0] = "file_lat_8procs0";
            files[1] = "file_lat_8procs1";
            files[2] = "file_lat_8procs2";
            files[3] = "file_lat_8procs3";
            files[4] = "file_lat_8procs4";
            files[5] = "file_lat_8procs5";
            files[6] = "file_lat_8procs6";
            files[7] = "file_lat_8procs7";

            filesize = 4194304 / 8;
      }
    }
    //if its for throughput for MBs/sec, name the appropriate amount of files
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
    else {
        //Assign num_procs and setup file arrays
        if(strcmp(argv[3], "1") == 0) {
            num_procs = 1;

<<<<<<< HEAD
            files[0] = "file1gb";
=======
            files[0] = "file_tp_1proc";
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

            filesize = 1073741824;
        } else if(strcmp(argv[3], "2") == 0) {
            num_procs = 2;

<<<<<<< HEAD
            files[0] = "file500-0";
            files[1] = "file500-1";
=======
            files[0] = "file_tp_2procs0";
            files[1] = "file_tp_2procs1";
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

            filesize = 524288000;
        } else if (strcmp(argv[3], "4") == 0) {
            num_procs = 4;

<<<<<<< HEAD
            files[0] = "file250-0";
            files[1] = "file250-1";
            files[2] = "file250-2";
            files[3] = "file250-3";
=======
            files[0] = "file_tp_4procs0";
            files[1] = "file_tp_4procs1";
            files[2] = "file_tp_4procs2";
            files[3] = "file_tp_4procs3";
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

            filesize = 262144000;
        } else if (strcmp(argv[3], "8") == 0) {
            num_procs = 8;

<<<<<<< HEAD
            files[0] = "file125-0";
            files[1] = "file125-1";
            files[2] = "file125-2";
            files[3] = "file125-3";
            files[4] = "file125-4";
            files[5] = "file125-5";
            files[6] = "file125-6";
            files[7] = "file125-7";
=======
            files[0] = "file_tp_8procs0";
            files[1] = "file_tp_8procs1";
            files[2] = "file_tp_8procs2";
            files[3] = "file_tp_8procs3";
            files[4] = "file_tp_8procs4";
            files[5] = "file_tp_8procs5";
            files[6] = "file_tp_8procs6";
            files[7] = "file_tp_8procs7";
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

            filesize = 131072000;
        }
    }

    //allocate buffer of argv[2] size
    char *buffer = aligned_alloc(512, sizeof(char)*block_size);

    //set start to starting time
    gettimeofday(&start, NULL); 
<<<<<<< HEAD

=======
    
    //set num_ops outside the loop
    num_ops = filesize / block_size;
    
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
    //forking process-ish

    //if specified to have more than 1 for num_procs
    if (num_procs > 1) {
<<<<<<< HEAD

=======
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
    //create num_procs number of children
    for (i = 0; i < num_procs; i++) {
        pid = fork();
        
<<<<<<< HEAD
        //start child process
        if (pid == 0) {
            //open the files
=======
        if (pid == 0) {
            //open the files for num_procs number of times
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
            fp = open(files[i], O_RDWR, O_DIRECT);

            //WS - write sequential
            if (strcmp(argv[1], "WS") == 0) {
<<<<<<< HEAD

                while(bytes_read < filesize){

=======
                while (bytes_read < filesize) {
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
                    //write sequential
                    bytes_read += write(fp, buffer, block_size);
                } 
            }
<<<<<<< HEAD
            //WR - write random
            else if (strcmp(argv[1], "WR") == 0) {
                upper = filesize - block_size;
                num_ops = filesize / block_size;
                i = 0;

                while (i < num_ops) {

                    //get a random number
                    int num = (rand() % (upper + 1));

                    //use lseek to go to a random location
                    lseek(fp, num, SEEK_SET);

                    //write random by buffer block size
                    bytes_read += write(fp, buffer, block_size);

=======

            //WR - write random
            else if (strcmp(argv[1], "WR") == 0) {
                limit = filesize - block_size;
                //num_ops = filesize / block_size;
                i = 0;

                while (i < num_ops) {
                    //get a random number
                    int num = (rand() % (limit + 1));
                    //use lseek to go to a random location
                    lseek(fp, num, SEEK_SET);
                    //write random by buffer block size
                    bytes_read += write(fp, buffer, block_size);
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
                    //increment loop
                    i++;
                } 
            } 

            //RS - read sequential
            else if (strcmp(argv[1], "RS" ) == 0){
<<<<<<< HEAD
                while(bytes_read < filesize) {
                    
=======
                while (bytes_read < filesize) {
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
                    //read sequential
                    bytes_read += read(fp, buffer, block_size);
                } 
            }
<<<<<<< HEAD
            //RR - read random
            else if (strcmp(argv[1], "RR") == 0){
                upper = filesize - block_size;
                num_ops = filesize / block_size;
                i = 0;

                while (i < num_ops) {

                //get a random number
                int num = (rand() % (upper + 1));

                //use lseek to go to a random location
                lseek(fp, num, SEEK_SET);

                //read random by buffer block size
                bytes_read += read(fp, buffer, block_size);

=======

            //RR - read random
            else if (strcmp(argv[1], "RR") == 0){
                limit = filesize - block_size;
                //num_ops = filesize / block_size;
                i = 0;

                while (i < num_ops) {
                //get a random number
                int num = (rand() % (limit + 1));
                //use lseek to go to a random location
                lseek(fp, num, SEEK_SET);
                //read random by buffer block size
                bytes_read += read(fp, buffer, block_size);
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
                //increment loop
                i++;
                } 
            } 

            //close each file after opening
            close(fp);
            exit(0);
        } 
    } 

    //parents waiting for children
    for(i = 0; i < num_procs;i ++){
        waitpid(pid, &status, WUNTRACED | WCONTINUED);
    }

    } 

    //when num_procs = 1 
<<<<<<< HEAD
    else { 

=======
    else { 	
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
        //open 1gb file
        fp = open(files[0], O_RDWR, O_DIRECT);

        //WS - write sequential
        if (strcmp(argv[1], "WS") == 0) {
            while (bytes_read < filesize) {
<<<<<<< HEAD

            //write sequential
            bytes_read += write(fp, buffer, block_size);
            } 
        }
        //WR - write random
        else if (strcmp(argv[1], "WR") == 0) {
            upper = filesize - block_size;
            num_ops = filesize / block_size;
            i = 0;

            while (i < num_ops) {
                //get a random number
                int num = (rand() % (upper + 1));

                //use lseek to go to a random location
                lseek(fp, num, SEEK_SET);

                //write random
                bytes_read += write(fp, buffer, block_size);

                i++;
            } 
        } 
        //RS - read sequential
        else if (strcmp(argv[1], "RS") ==0 ){
            while (bytes_read < filesize) {
                
=======
            	//write sequential
            	bytes_read += write(fp, buffer, block_size); 
            } 
        }

        //WR - write random
        else if (strcmp(argv[1], "WR") == 0) {
            limit = filesize - block_size;
            //num_ops = filesize / block_size;
            i = 0;
  
            while (i < num_ops) {
                //get a random number
                int num = (rand() % (limit + 1));
                //use lseek to go to a random location
                lseek(fp, num, SEEK_SET);
                //write random
                bytes_read += write(fp, buffer, block_size);
                //increment loop
                i++;
            } 
        } 

        //RS - read sequential
        else if (strcmp(argv[1], "RS") == 0 ){
            while (bytes_read < filesize) {
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
                //read sequential
                bytes_read += read(fp, buffer, block_size);
            } 
        } 
<<<<<<< HEAD
        //RR - read random
        else if (strcmp(argv[1], "RR") == 0){
            upper = filesize - block_size;
            num_ops = filesize/block_size;
            i = 0;

            while(i < num_ops){

                //get a random number
                int num = (rand() % (upper + 1));

                //use lseek to go to a random location
                lseek(fp, num, SEEK_SET);

                //write random
                bytes_read += read(fp, buffer, block_size);

                //increment
=======

        //RR - read random
        else if (strcmp(argv[1], "RR") == 0){
            limit = filesize - block_size;
            //num_ops = filesize/block_size;
            i = 0;

            while (i < num_ops) {
                //get a random number
                int num = (rand() % (limit + 1));
                //use lseek to go to a random location
                lseek(fp, num, SEEK_SET);
                //write random
                bytes_read += read(fp, buffer, block_size);
                //increment loop
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
                i++;
            } 
        }

        close(fp);

    } 

    //set end to ending time
    gettimeofday(&end, NULL);

    //free the allocated memory buffer
    free(buffer);

    //find time taken by subtracting end time by start time (in seconds)
<<<<<<< HEAD
    time = (double)(end.tv_sec - start.tv_sec) + (double)(end.tv_usec - start.tv_usec)/1000000;
=======
    double time = (double)(end.tv_sec - start.tv_sec) + (double)(end.tv_usec - start.tv_usec)/1000000;
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af

    //double time_elapsed = (end.tv_sec * 1000000 + end.tv_usec) - (start.tv_usec * 1000000 + start.tv_usec));
    //multiply by 1e-6 to convert microseconds to seconds

    //latency output
<<<<<<< HEAD
    if (argc == 5 && strcmp(argv[4], "-O") == 0) { 

        //to get OPs/s for latency
        opsPerSec = (num_ops * num_procs) / time;  //equation checked from piazza as well? 

        //print it out directly
        printf("%f OPs/s\n", opsPerSec);
=======
    if (argc == 5 && (strcmp(argv[4], "-O") == 0)) { 

        //to get OPs/s for latency
        double OPs = (num_ops * num_procs) / time;  //equation checked from piazza as well? 
        printf("%f OPs/s\n", OPs);
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
    }
    //throughput output
    else {
        //to get MB/s for throughput
<<<<<<< HEAD
        MBperS = (filesize / 1024 / 1204) / time;

        //print output
        printf("%f MB/sec\n", MBperS);
=======
        double MBs = ((filesize*num_procs) / 1024 / 1024) / time;
        printf("%f MB/sec\n", MBs);
>>>>>>> 459fb237e28624b065a6b5c22ac83b5f11edf2af
    }

    return 0;
} 

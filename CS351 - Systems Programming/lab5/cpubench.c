#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>
#include <sys/time.h>
#include <sys/types.h>
#include <wait.h>
#include <stdint.h>
#include <pthread.h>

#define MSG "* running cpubench %s using %s with size %s and %s threads...\n"

#define USAGE "usage: ./cpubench <mode> <type> <size> <threads> \n" \
"     - mode: flops / matrix \n" \
"     - type: single / double \n" \
"     - size: small / medium / large \n" \
"     - threads: 1 / 2 / 4 \n"

#define GIGAFLOPS 1000000000
#define GIGABYTES 1024*1024*1024

// This function multiplies mat1[][] and mat2[][],
// and stores the result in res[][]

int **matrixint1;
int **matrixint2;
int **res;

double **matdouble1;
double **matdouble2;
double **resd;

int size;
int num_threads;
int type;

void *multiply(void *arg) {
	int pos = (int)arg;
	int row = size/num_threads;
	int s = row * pos;
	int e = s + row;
	for (int i = s; i < e; ++i) {
		for (int j = 0; j < size; ++j) {
			for (int k = 0; k < size; ++k) {
				if(type == 0){
					res[i][j] += matrixint1[i][k] * matrixint2[k][j];
				}
				else{
					resd[i][j] += matdouble2[i][k] * matdouble2[k][j];
				}
			}
		}
	}
}

//single threading matrix multiplication
//for (int i = 0; i < m; i++) {
//  for (int j = 0; j < n; j++) {
//    for (int p = 0; p < k; p++) {
//      C(i, j) += A(i, p) * B(p, j);
//    }
//  }
//}


//LoadFloat8?
//BroadcastFloat8?
//AdduFloat8?

double randd(double min, double max) {
    double range = (max - min); 
    double div = RAND_MAX / range;
    return min + (double)(rand() / div);
}

void fill() {
	int *buffer;

	if (type == 0) {		 
		int len = sizeof(int *) * size + sizeof(int) * size * size;
		matrixint1 = (int **)malloc(len); 
		matrixint2 = (int **)malloc(len); 
		res = (int **)malloc(len); 

		buffer = (int *)(matrixint1 + size); 
		for (int i = 0; i < size; i++) 
        matrixint1[i] = (buffer + size * i);

		buffer = (int *)(matrixint2 + size); 
		for (int i = 0; i < size; i++) 
        matrixint2[i] = (buffer + size * i);

		buffer = (int *)(res + size); 
		for (int i = 0; i < size; i++) 
        res[i] = (buffer + size * i);

	} else {
		int len = sizeof(double *) * size + sizeof(double) * size * size;
		matdouble2 = (double **)malloc(len); 
		matdouble2 = (double **)malloc(len); 
		resd = (double **)malloc(len); 

		buffer = (double *)(matdouble2 + size); 
		for (int i = 0; i < size; i++) 
        matdouble2[i] = (buffer + size * i);

		buffer = (double *)(matdouble2 + size); 
		for (int i = 0; i < size; i++) 
        matdouble2[i] = (buffer + size * i);

		buffer = (double *)(resd + size); 
		for (int i = 0; i < size; i++) 
        resd[i] = (buffer + size * i);
	}	

	for (int i = 0; i < size; ++i) {
		for (int j = 0; j < size; ++j) {
			if (type == 0) {
				matrixint1[i][j] = rand() % 100;
				matrixint2[i][j] = rand() % 100;
				res[i][j] = 0;
			} else {
				matdouble2[i][j] = (double)(rand() % 100);
				matdouble2[i][j] = (double)(rand() % 100);
				resd[i][j] = 0.0;
			}					
		}
	}
}



long long compute_flops_int(int size) {
	long long index;
	long long result;
	long long loops = size * (unsigned long long) GIGAFLOPS;
	for (index = 0; index < loops; index++) {
		result = index+1;
	}
	return result;
}

double compute_flops_double(int size) {
	long long index;
	double result;
	long long loops = size * (unsigned long long) GIGAFLOPS;
	for (index=0;index<loops;index++) {
		result = index+1.0;
	}
	return result;
}


int main(int argc, char **argv) {
	time_t t;
	srand((unsigned) time(&t));
    if (argc != 5) {
        printf(USAGE);
        exit(1);
    } else {
		int mode;

        if (strcmp(argv[1],"flops") == 0)
        	mode = 0;
        else if(strcmp(argv[1],"matrix") == 0)
        	mode = 1;
        else
        	mode = -1;

        if(strcmp(argv[2],"single") == 0)
        	type = 0;
        else if(strcmp(argv[2],"double") == 0)
        	type = 1;
        else
        	type = -1;


		if(strcmp(argv[3],"small") == 0)
        	size = mode ? 1024:10;
        else if(strcmp(argv[3],"medium") == 0)
        	size = mode ? 4096:100;
		else if(strcmp(argv[3],"large") == 0)
			size = mode ? 16384:1000;
        else
        	size = -1;

        num_threads = atoi(argv[4]);

		if(mode == 1){
			fill();
		}

		struct timeval start, end;
		
		FILE * fp;
		fp = fopen("/dev/null", "w");
		gettimeofday(&start, NULL);
		if (mode == 0) {
			int tsize = size/num_threads;
			for (int i = 0; i < num_threads; i++) {
				int pid;
				if ((pid=fork())==0) {
					if (type == 0) {	
						long long volatile i = compute_flops_int(tsize);
						fprintf(fp,"%lld",i);
					} else if (type == 1) {	
						double volatile i = compute_flops_double(tsize);
						fprintf(fp,"%d",i);
					} else {
						printf(USAGE);
						printf("unrecognized option, exiting...\n");
						exit(1);
					}
					exit(0);
				}
			}
			int status;
			while (wait(&status) > 0);
		}
		else if (mode == 1) {
			pthread_t pt[num_threads];
			int rp;
			void *stat;
			for (int i = 0; i < num_threads; i++) {
				if (rp = pthread_create(&pt[i], NULL, *multiply, (void *)i)) {
					printf("Pthread failed");
					exit(1);
				}
			}
			for (int i = 0 ;i < num_threads; i++) {
				pthread_join(pt[i],&stat);
			}
			if (type==0) {
				fprintf(fp,"%i",res[0][0]);
			} else {
				fprintf(fp,"%d",resd[0][0]);
			}			
		}
		
		fclose(fp);
		gettimeofday(&end, NULL);

		double elapsed_time_sec = (((end.tv_sec * 1000000 + end.tv_usec) - (start.tv_sec * 1000000 + start.tv_usec)))/1000000.0;
		double num_giga_ops = 0;
		
		if (size*(unsigned long long)GIGAFLOPS < 0) {
			printf("error in size, check for overflow; exiting...\n");
			exit(1);
		}
		if (elapsed_time_sec < 0) {
			printf("error in elapsed time, check for proper timing; exiting...\n");
			exit(1);
		}
		if (elapsed_time_sec == 0) {
			printf("elapsed time is 0, check for proper timing or make sure to increase amount of work performed; exiting...\n");
			exit(1);
		}
			
		
		if (mode == 0)
			num_giga_ops = size;
		else if (mode == 1)
			num_giga_ops = size*size*size/(GIGABYTES);

		double throughput = num_giga_ops/elapsed_time_sec;

		printf("mode=%s type=%s size=%i threads=%d time=%lf throughput=%lf\n",argv[1],argv[2],size,num_threads,elapsed_time_sec,throughput);
 
    }

    return 0;
}

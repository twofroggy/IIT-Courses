#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>
#include <math.h>
#include <sys/time.h>
#include <stdbool.h> 

#define MSG "running matrixadd with size %s...\n"

#define USAGE "usage: ./matrixadd <size> \n" \
"     - size: 10 / 100 / 1000 / 10000 \n" \


// This function adds mat1[][] and mat2[][],
// and stores the result in res[][]
void add(double** mat1, double** mat2, double** res, int size)
{
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			res[i][j] = mat1[i][j] + mat2[i][j];
		}
	}
}

// This function finds the minimum value in res[][] array
double min(double** res, int size)
{
	double minimum = res[0][0];
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			if (res[i][j] < minimum) {
				minimum = res[i][j];
			}
		}
	}
	return minimum;
}

// This function finds the average value in res[][] array
double aver(double** res, int size)
{
	double tot = 0.0;
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			tot += res[i][j];
		}
	}
	return tot/size;
}

// This function finds the maximum value in res[][] array
double max(double** res, int size)
{
	double maximum = res[0][0];
	for (int i = 0; i < size; i++) {
		for (int j = 0; j<size; j++) {
			if (res[i][j] > maximum) {
				maximum = res[i][j];
			}
		}
	}
	return maximum;
}

int main(int argc, char **argv)
{
	time_t t;
	srand((unsigned) time(&t));
    if (argc != 2) 
    {
        printf(USAGE);
        exit(1);
    } 
    else 
    {
        printf(MSG, argv[1]);
        int size = atoi(argv[1]);
		struct timeval start, end;
		size_t len = 0;

		//declare arr1, arr2, and arr3
		double **arr1 = NULL, **arr2 = NULL, **arr3 = NULL;
		//allocate memory for arr1, arr2, and arr3 as a 2D array with size provided by command line argument
    	printf("allocating %lf GB memory...\n",len*3.0/(1024*1024*1024)); 
		//initialize arr1 and arr2 to random double values between 0 and 1

		//get start timestamp
  		gettimeofday(&start, NULL);

		printf("add arr1 and arr2 and store it in arr3\n");
		add(arr1,arr2,arr3,size);
		printf("min(arr3)=%lf\n",min(arr3,size));
		printf("aver(arr3)=%lf\n",aver(arr3,size));
		printf("max(arr3)=%lf\n",max(arr3,size));

		//get end timestamp
		 gettimeofday(&end, NULL);

		double elapsed_time_us = ((end.tv_sec * 1000000 + end.tv_usec) - (start.tv_sec * 1000000 + start.tv_usec));
		printf("matrixadd with size %d ==> %lf sec\n",size,elapsed_time_us/1000000.0);
    }

    return 0;
}

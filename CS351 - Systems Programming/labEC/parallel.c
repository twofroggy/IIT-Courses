#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/wait.h> 
#include <sys/types.h>

int main(int argc, char *argv[])
{
	//if number of arguments are less than 4 (including ./parallel)
	if (argc < 4) {
		printf("incorrect number of arguments, %s needs 4\n", argv[0]);
		exit(1);
	}

	//if the first arugment after ftn is an integer
	int n = 0;
	int x = 0;
	while (argv[1][x] != '\0')  { 
		if (argv[1][x] < '0' || argv[1][x] > '9') { 
			printf("Entered argument is not an integer\n");
			exit(1);
		}
		x++;
		n++;
	}

	//declaring int i for for loop and separating out the args from input to another array
	int i;
	int count = atoi(argv[1]); //number of times to repeat the cmd
//	char *buffer[argc - 2]; //array for cmd and time
	//put cmd argument and time argument into the buffer array
//	for (j = 2; j < argc; j++) {
//		buffer[j-2] = argv[j];
//	}
	
	int c = 0 ;
	//loops the forking process
	for (i = 0; i < count; i++) {
		if (fork() == 0) {
			//execvp(argv[2], &argv[2]);
			//check if execvp<0 bc that means it didnt work then
			if (execvp(argv[2], &argv[2]) < 0) {
				c = 1;
				printf("child %d failed: Could not execvp\n", i+1); 
				exit(1);
			} 
		}
	} 
	int k;
	for (k = 0; k < count; k++) {
		wait(NULL);
	} 
	if (c == 1) {
		printf("FAILED in running %d parallel %s tasks\n", count, argv[2]);
	} else {
		printf("SUCCESS in running %d parallel %s tasks\n", count, argv[2]);
	}
} 

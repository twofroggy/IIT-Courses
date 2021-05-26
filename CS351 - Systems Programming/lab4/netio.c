#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>

#include <sys/time.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include "functions.h"
#include "pipe-server.h"
#include "data.h"

#define R 0
#define W 1
#define PORT 8080 

#define MSG "* running netio with method %s operation %s for %s number of ops...\n"

#define USAGE "usage: ./netio <method> <operation> <num_ops> \n" \
"     - method: function / pipe / socket / rpc \n" \
"     - operation: add / subtract / multiply / divide \n" \
"     - num_calls: 1000 | 1000000 \n"

//moved the operation functions to functions.h

int main(int argc, char **argv)
{
	Data data;
	time_t t;
	srand((unsigned) time(&t));
	int method = -1; //used to store what method to test
	int operation = -1; //used to store what operation to test
    if (argc != 4) 
    {
        printf(USAGE);
        exit(1);
    } 
    else 
    {
        printf(MSG, argv[1], argv[2], argv[3]);
        if(strcmp(argv[1],"function") == 0)
        	method = 0;
        else if(strcmp(argv[1],"pipe") == 0)
        	method = 1;
        else if(strcmp(argv[1],"socket") == 0)
        	method = 2;
        else if(strcmp(argv[1],"rpc") == 0)
        	method = 3;
        else
        	method = -1;

        if(strcmp(argv[2],"add") == 0)
        	operation = 0;
        else if(strcmp(argv[2],"subtract") == 0)
        	operation = 1;
        else if(strcmp(argv[2],"multiply") == 0)
        	operation = 2;
        else if(strcmp(argv[2],"divide") == 0)
        	operation = 3;
        else
        	operation = -1;

        int num_calls = atoi(argv[3]);

		struct timeval start, end;

  		gettimeofday(&start, NULL);

		double ret_value = 0.0;

   		switch (method)
     	{
        	case 0:			//function method
   				switch (operation)
     			{
        			case 0:			//add
           				for (int i=0;i<num_ops;i++)
           					ret_value = add((double)rand()/RAND_MAX,(double)rand()/RAND_MAX);
           				break;
        			case 1:			//subtract
           				for (int i=0;i<num_ops;i++)
           					ret_value = subtract((double)rand()/RAND_MAX,(double)rand()/RAND_MAX);
           				break;
        			case 2:			//multiply
           				for (int i=0;i<num_ops;i++)
           					ret_value = multiply((double)rand()/RAND_MAX,(double)rand()/RAND_MAX);
           				break;
        			case 3:			//divide
           				for (int i=0;i<num_ops;i++)
           					ret_value = divide((double)rand()/RAND_MAX,(double)rand()/RAND_MAX);
           				break;
        			default:
           				printf("operation not supported, exit...\n");
           				return -1;
     			}		
     			break;
        	case 1:			//pipe method
				
				//create the file descriptors to open the pipes to
				data.op = operation;
				int serverTo[2];
				int serverFrom[2];
				//pipe to
				pipe(serverTo);
				pipe(serverFrom);

				if(fork()==0){
					//close pipes
					close(serverTo[W]);
					close(serverFrom[R]);

					//pipe the server
					pipeServer(serverTo[0],serverFrom[1],num_ops);

					//close pipes again
					close(serverTo[R]);
					close(serverFrom[W]);

					//exit code
					exit(0);					
				}	//end of if fork
				else {
					//close pipes
					close(serverTo[R]);
					close(serverFrom[W]);

					//for loop to get random numbers and then write and read to pipe
					for (int i = 0; i < num_ops; i++) {
						//make two random numbers
						data.num1 = (double)rand()/RAND_MAX;
						data.num2 = (double)rand()/RAND_MAX;	
						//write to pipe 
						write(serverTo[1], &data, sizeof(data));
						read(serverFrom[0], &ret_value, sizeof(double));
					}	//end of for loop
					close(serverTo[W]);
					close(serverFrom[R]);
				}		//end of else in the if statement
     			break;

        	case 2:		//socket method 

				//declare variables
				data.op = operation;
   	  			int sock = 0, valread; 
				struct sockaddr_in serv_addr; 

				//if statement for error fail safe
				if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) { 
					printf("\n Socket creation error \n"); 
					return -1; 
				} //end of if statement

				serv_addr.sin_family = AF_INET; 
				serv_addr.sin_port = htons(PORT); 
				
				//Convert IPv4 and IPv6 addresses from text to binary form 
				if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) { 
					printf("\nInvalid address/ Address not supported \n"); 
					return -1; 
				} //end of if statement for error address
			
				if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) { 
					printf("\nConnection Failed \n"); 
					return -1; 
				} //end of if statement for connection fail

				for (int i = 0; i < num_ops; i++) {
					//make two random numbers
					data.num1 = (double)rand()/RAND_MAX;
					data.num2 = (double)rand()/RAND_MAX;		

					//send data to the socket			
					send(sock, &data,sizeof(data) ,0); 

					//read data from socket
					read(sock, &ret_value, sizeof(double)); 
				}
     			break;

			case 3:		//rpc method for extra credit
				switch (operation)
				{
					case 0:
						printf("%s %s %s\n",argv[1],argv[2],argv[3]);
						break;
					case 1:
						printf("%s %s %s\n",argv[1],argv[2],argv[3]);
						break;
					case 2:
						printf("%s %s %s\n",argv[1],argv[2],argv[3]);
						break;
					case 3:
						printf("%s %s %s\n",argv[1],argv[2],argv[3]);
						break;
					default:
						printf("operation not supported, exit...\n");
						return -1;
				}		
			break;
				
			default:
				printf("method not supported, exit...\n");
				return -1;
     	}		

     	gettimeofday(&end, NULL);

		double elapsed_time_us = ((end.tv_sec * 1000000 + end.tv_usec) - (start.tv_sec * 1000000 + start.tv_usec));
		printf("==> %f ops/sec\n",(num_ops/elapsed_time_us)*1000000);
 
    }

    return 0;
}

#include "pipe-server.h"
#include "data.h"
#include "functions.h"

void pipeServer(int r_end, int w_end, int num_calls) {
    Data data;
    double r;
    
    //create the FIFO (named pipe) 
   	//mkfifo(client_to_server_pipe, 0666);
	//mkfifo(server_to_client_pipe, 0666);


    for (int i = 0; i < num_calls; i++) {
        r = 0.0;
        read(r_end,&data, sizeof(data));
        switch (data.op)
        {            
            case 0:						
                r = add(data.num1, data.num2);
                break;
            case 1:
                r = subtract(data.num1, data.num2);                
                break;
            case 2:
                r = multiply(data.num1, data.num2);
                break;
            case 3:
                r = divide(data.num1, data.num2);
                break;
            default:
                printf("operation not supported, exit...\n");
        }
        //read(server_to_client, buf2, 2);
        write(w_end, &r, sizeof(double));
    }
}

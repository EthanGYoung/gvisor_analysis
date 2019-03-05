#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>


int NUM_TRIALS;
int MALLOC_SIZE;

// Gets the current time
struct timespec diff(struct timespec start, struct timespec end)
{
        struct timespec temp;
        if ((end.tv_nsec - start.tv_nsec) < 0)
        {
                temp.tv_sec = end.tv_sec - start.tv_sec - 1;
                temp.tv_nsec = 1000000000 + end.tv_nsec - start.tv_nsec;
        }
        else
        {
                temp.tv_sec = end.tv_sec - start.tv_sec;
                temp.tv_nsec = end.tv_nsec - start.tv_nsec;
        }
        return temp;
}


float execute() {
        char *str;

        // Start timer
        struct timespec ts0;
        clock_gettime(CLOCK_REALTIME, &ts0);

        for (int i = 0; i < NUM_TRIALS; i++) {
                //malloc
                str = (char *) malloc(MALLOC_SIZE);
                strcpy(str, "test");
                if(strcmp(str,"test") != 0) {
                        printf("ERROR: Failed to read from str\n");
                        return 0;
                }
                //free
                free(str);
        }

        // End timer
        struct timespec ts1;
        clock_gettime(CLOCK_REALTIME, &ts1);
        struct timespec t = diff(ts0,ts1);
        //close(fd);
        float elapsed_time = t.tv_sec + t.tv_nsec/(float)1000000000;

        return elapsed_time;
}

int main(int argc, char *argv[]) {
        // Parse command line args
        if (argc != 3) {
                printf("ERROR: Usage: ./mallocfree <number of trials> <malloc size>\n");
                return 0;
        }


        NUM_TRIALS = atoi(argv[1]);

        float total = 0;

        total = execute();

        printf("LOG_OUTPUT: Average for %d trials: Open/close time average = %.12f seconds\n", NUM_TRIALS, total/NUM_TRIALS);

        return 0;
}

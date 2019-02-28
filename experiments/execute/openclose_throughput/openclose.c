#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdlib.h>

int NUM_TRIALS;
int READ_SIZE;
char* FILE_PATH = "./placeholder.txt";

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


float execute(char *file) {
        int fd, ret;

        // Start timer
        struct timespec ts0;
        clock_gettime(CLOCK_REALTIME, &ts0);

	for (int i = 0; i < NUM_TRIALS; i++) {
		// Open file
		fd = open(file, O_CREAT|O_RDWR );
		if (fd == -1) {
			perror ("ERROR: open");
			return 1;
		}
	
		// Close file
		ret = close(fd);
		if (ret == -1) {
			perror("ERROR: close");
			return 1;
		}
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
        if (argc != 2) {
                printf("ERROR: Usage: ./openclose <number of trials>\n");
                return 0;
        }


        NUM_TRIALS = atoi(argv[1]);

        float total = 0;

        total = execute(FILE_PATH);

        printf("LOG_OUTPUT: Average for %d trials: Open/close time average = %.12f seconds\n", NUM_TRIALS, total/NUM_TRIALS);

        return 0;
}

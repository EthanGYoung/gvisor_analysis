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
char* FILE_PATH;
int INMEM_FLAG = 346;

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
        int fd, fd_WR;

        // Open the specific file inmem
        fd_WR = open(file, O_WRONLY|O_CREAT);
        if (fd == 0) {
                perror ("ERROR: open");
                return 1;
        }

	char *init_write = calloc(1000*READ_SIZE, sizeof(char));
        char data[READ_SIZE];
        int r = 0;
        int total_read = 0;

		
	int written = write(fd_WR, init_write, 1000*READ_SIZE); 
	if (written != READ_SIZE*1000) {
		printf("Unable to write total");
	}
        fd = open(file, O_RDONLY);
        if (fd == 0) {
                perror ("ERROR: open");
                return 1;
        }
        // Start timer
        struct timespec ts0;
        clock_gettime(CLOCK_REALTIME, &ts0);

	for (int i = 0; i < NUM_TRIALS; i++) {
		if ((NUM_TRIALS % 1000) == 0) {
			lseek(fd, 0, SEEK_SET);
		}

		// Reads total read size
		if ( (r = read(fd, data, READ_SIZE)) == READ_SIZE) {
			total_read = total_read + r;
		} else {
			printf("ERROR: Was not able to read READ_SIZE. Trial num is: %d\n", i);
			exit(1);
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
        if (argc != 4) {
                printf("ERROR: Usage: ./read <number of trials> <size of file read in Bytes> <path to rile to read>\n");
                return 0;
        }


        NUM_TRIALS = atoi(argv[1]);
        READ_SIZE = atoi(argv[2]);
	FILE_PATH = argv[3];

        float total = 0;

        total = execute(FILE_PATH);

        printf("LOG_OUTPUT: Average for %d trials and READ_SIZE = %d: Read time average = %.12f seconds\n", NUM_TRIALS, READ_SIZE, total/NUM_TRIALS);

        return 0;
}

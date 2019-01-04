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
        int fd;

        // Open the specific file
        fd = open(file, O_RDONLY);
        if (fd == 0) {
                perror ("open");
                return 1;
        }

        char data[READ_SIZE];
        int r = 0;
        int total_read = 0;

        // Start timer
        struct timespec ts0;
        clock_gettime(CLOCK_REALTIME, &ts0);

        // Writes the whole file
	if ( (r = read(fd, data, READ_SIZE)) == READ_SIZE) {
                total_read = total_read + r;
        }
        // End timer
        struct timespec ts1;
        clock_gettime(CLOCK_REALTIME, &ts1);
        struct timespec t = diff(ts0,ts1);

        // Remove the file
        //remove(file);

        close(fd);
        float elapsed_time = t.tv_sec + t.tv_nsec/(float)1000000000;

        return elapsed_time;
}

int main(int argc, char *argv[]) {
        // Parse command line args
        if (argc != 3) {
                printf("Usage: ./driver <number of trials> <size of file write in Bytes>\n");
                return 0;
        }


        NUM_TRIALS = atoi(argv[1]);
        READ_SIZE = atoi(argv[2]);

        float total = 0;
        float trial_val = 0;

        for (int i = 0; i < NUM_TRIALS; i++) {
                trial_val = execute("./file.txt");
                total += trial_val;
        }

        printf("Average for %d trials and READ_SIZE = %d: Read time = %f seconds, %f bytes/second\n", NUM_TRIALS, READ_SIZE, total/NUM_TRIALS, READ_SIZE*NUM_TRIALS/total);

        return 0;
}


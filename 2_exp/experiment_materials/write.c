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
int WRITE_SIZE;

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
        fd = open(file, O_WRONLY|O_CREAT);
        if (fd == 0) {
                perror ("open");
                return 1;
        }

        char *data = calloc(WRITE_SIZE, sizeof(char));
        int r = 0;
        int total_written = 0;

        // Start timer
        struct timespec ts0;
        clock_gettime(CLOCK_REALTIME, &ts0);

        // Writes the whole file
        if ( (r = write(fd, data, WRITE_SIZE)) == WRITE_SIZE)
                total_written = total_written + r;

        // End timer
        struct timespec ts1;
        clock_gettime(CLOCK_REALTIME, &ts1);
        struct timespec t = diff(ts0,ts1);

        // Remove the file
        remove(file);

        //printf( "Done opening and writing. %d bytes written in %d seconds and %ld nanoseconds.\n", total_written, t.tv_sec, t.tv_nsec);
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
        WRITE_SIZE = atoi(argv[2]);

        float total = 0;
        float trial_val = 0;

        for (int i = 0; i < NUM_TRIALS; i++) {
                trial_val = execute("./file.txt");
        //      printf("Trial %d: Write time = %f seconds, %f bytes/second\n", i+1, trial_val, WRITE_SIZE/trial_val);
                total += trial_val;
        }

        printf("\n\nAverage for %d trials and WRITE_SIZE = %d: Write time = %f seconds, %f bytes/second\n\n", NUM_TRIALS, WRITE_SIZE, total/NUM_TRIALS, WRITE_SIZE*NUM_TRIALS/total);

        return 0;
}

#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdlib.h>

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


float execute(int NUM_CALLS) {
	struct timespec ts0;
        clock_gettime(CLOCK_REALTIME, &ts0);

	// Run test
	for (int i = 0; i < NUM_CALLS; i++) {
		getpid();
	}

	// Edn timer
	struct timespec ts1;
        clock_gettime(CLOCK_REALTIME, &ts1);
        struct timespec t = diff(ts0,ts1);

        float elapsed_time = t.tv_sec + t.tv_nsec/(float)1000000000;
        return elapsed_time;
}

int main(int argc, char *argv[]) {
	// Parse command line args
	if (argc != 2) {
                printf("ERROR: Usage: ./driver <number of calls>\n");
                return 0;
        }


        int NUM_CALLS = atoi(argv[1]);

        float total = 0;

        total = execute(NUM_CALLS);

        printf("LOG_OUTPUT: Average for %d calls: getpid syscall time average = %.12f seconds\n", NUM_CALLS, total/NUM_CALLS);

        return 0;
}

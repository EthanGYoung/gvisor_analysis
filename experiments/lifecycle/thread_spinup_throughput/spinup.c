#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>

pthread_t *threads;
int *IDs;
float *trial_results;
float *overall_results; // Total throughput for each test

int RUNC = 0;
char* RUNTIME;

int NUM_SPINUPS;

// Determines the difference in time between two timespec structs
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

// Function that each thread is running
void *spinup(void *id) {
        int thread_id = *(int*)id;

        // Start timer
        struct timespec ts0;
        clock_gettime(CLOCK_REALTIME, &ts0);

        // Spinup and kill NUM_SPINUPS images
        for (int i = 0; i < NUM_SPINUPS; i++) {
		char str[100];
		strcpy(str, "sudo docker run --runtime=");
		strcat(str, RUNTIME);
		strcat(str, "  --rm no_op");
        	system(str);
        }

        // End timer
        struct timespec ts1;
        clock_gettime(CLOCK_REALTIME, &ts1);
        struct timespec t = diff(ts0,ts1);

        // Save result (images/second)
        float elapsed_time = t.tv_sec + t.tv_nsec/(float)1000000000; // Time elapsed in seconds
        trial_results[thread_id] = NUM_SPINUPS/elapsed_time;
	return NULL;
}

float calculate_stats(int num_threads) {
        float total = 0;

        for (int i = 0; i < num_threads; i++) {
                total += trial_results[i];
        }

        return total;
}
// Begins each thread and waits for each completion
float start_threads(int num_threads) {
        // Starts all threads with time limit equal to seconds
        for (int i = 0; i < num_threads; i++) {
        //      printf("Starting thread %d\n", i);
                pthread_create(&threads[i], NULL, spinup, &(IDs[i]));
        }

        // Joins all threads when they complete
        for (int i = 0; i < num_threads; i++) {
                pthread_join(threads[i], NULL);
        }

        // Calculate statistics (total throughput)
        return calculate_stats(num_threads);
}

// Print the results of the threads and then avg them
void report_trial_results(int num_threads) {
        float total = 0;

        for (int i = 0; i < num_threads; i++) {
                printf("Throughput for thread %d is %f images/second\n", i, trial_results[i]);
                total += trial_results[i];
        }

        printf("\n\n\nAverage throughput is %f images/second\n", total/num_threads);
        printf("Total throughput is %f images/second\n", total);
}

// Tests for given num threads
int drive(int num_threads, int num_trials)
{
        // Initialize global variables
        threads = (pthread_t *)malloc(num_threads * sizeof(pthread_t));
        IDs = (int *)malloc(num_threads * sizeof(int));
        for (int i = 0; i < num_threads; i++) {
                IDs[i] = i;
        }

        trial_results = (float *)malloc(num_threads * sizeof(float));
        overall_results = (float *)malloc(num_trials * sizeof(float));

        float total = 0;
        
	for (int i = 0; i < num_trials; i++) {
                // Start X number of threads to start up docker containers (no-op)
                overall_results[i] = start_threads(num_threads);
                total += overall_results[i];
                printf("Throughput for trial %d is %f images/second\n", i+1, overall_results[i]);
        }

        // Print the results
        printf("Num threads: %d Average throughput is %f images/second\n", num_threads, total/num_trials);
	
	return 0;
}

int main(int argc, char *argv[]) {
        // Parse command line args
        if (argc != 5) {
                printf("Usage: ./driver <max number of threads> <number of trials> <runtime> <number of spinups per thread>\n");
                return 0;
        }

        int max_num_threads = atoi(argv[1]);
        int num_trials = atoi(argv[2]);
	RUNTIME = argv[3];
	NUM_SPINUPS = atoi(argv[4]);
        
	for (int i = 0; i < max_num_threads; i++) {
                printf("Running with %d threads\n", i+1);
                drive(i+1, num_trials);
        }
}

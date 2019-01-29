#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int NUM_TRIALS;
char* URL;

int main(int argc, char *argv[]) {
	// Parse command line args
	if (argc != 3) {
                printf("ERROR: Usage: ./driver <number of trials> <URL to curl>\n");
                return 0;
        }


        NUM_TRIALS = atoi(argv[1]);
        URL = argv[2];

        float total = 0;
        float trial_val = 0;

        for (int i = 0; i < NUM_TRIALS; i++) {
                printf("Trial: %d URL: %s\n", i+1, URL);
                fflush(stdout);
                char str[1000];
                strcpy(str, "curl -so /dev/null -w 'LOG_OUTPUT: %{time_total} seconds\n' ");
                strcat(str, URL);
                system(str);
        }


        return 0;
}

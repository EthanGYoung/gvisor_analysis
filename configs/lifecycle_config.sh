#!/bin/bash

#### Constants ####

TEST_LIFECYCLE_LIST=()

TEST_FILE="test.sh"

#### lifecycle ####


# thread_spinup_throughput
THREAD_FOLDER_PATH="experiments/execute/thread_spinup_throughput/"
THREAD_APP_NAME="spinup"
THREAD_SPINUP_NUM_THREADS=1
THREAD_SPINUP_NUM_TRAILS=2
THREAD_SPINUP_NUM_SPINUPS_PER_THREAD=1


	# Generate list of tests
generate_cmds() {
  RUNTIME=$1

	# Thread_throughput
	#TEST_LIFECYCLE_LIST+="$THREAD_FOLDER_PATH $THREAD_APP_NAME $THREAD_SPINUP_NUM_THREADS $THREAD_SPINUP_NUM_TRIALS $THREAD_SPINUP_NUM_SPINUPS_PER_THREAD"

}

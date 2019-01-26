#!/bin/bash

source config.sh

generate_cmds() {
	RUNTIME=$1

	# Spin up
	TEST_SPINUP_LIST[0]="experiments/spinup/run.sh"

	# Import
	TEST_IMPORT_LIST[0]="experiments/import/run.sh"

	# Execute
	TEST_EXECUTE_LIST[0]="experiments/execute/getpid_throughput/test.sh
			      	$GETPID_APP_NAME
				$RUNTIME
				$GETPID_NUM_CALLS"
	TEST_EXECUTE_LIST[1]="experiments/execute/network_throughput/test.sh
			      	$NETWORK_APP_NAME
				$RUNTIME
				$NETWORK_TRAILS
			     	$NETWORK_URL"
	TEST_EXECUTE_LIST[2]="experiments/execute/read_throughput/test.sh
			      	$READ_APP_NAME
				$RUNTIME
				$READ_TRAILS
			      	$READ_READ_SIZE
				$READ_FILE"
	TEST_EXECUTE_LIST[3]="experiments/execute/write_throughput/test.sh
				$WRITE_APP_NAME
				$RUNTIME
				$WRITE_TRAILS
			      	$WRITE_WRITE_SIZE
			      	$WRITE_FILE"
	# Lifecycle
	TEST_LIFECYCLE_LIST[0]="experiments/execute/thread_spinup_throughput/test.sh
				$THREAD_APP_NAME
				$RUNTIME
				$THREAD_SPINUP_NUM_THREADS
				$THREAD_SPINUP_NUM_TRAILS
				$THREAD_SPINUP_NUM_SPINUPS_PER_THREAD"
}


echo "Test Suite Initializing..."

echo "Test Suite executing on bare metal"

generate_cmds "bare"

TEST_LIST=( "${TEST_SPINUP_LIST[@]}" \
            "${TEST_IMPORT_LIST[@]}" \
            "${TEST_EXECUTE_LIST[@]}" \
            "${TEST_LIFECYCLE_LIST[@]}" \
          )

for i in "${TEST_LIST[@]}"
do
  echo "Initializing test: $i"
  /bin/bash $i
done

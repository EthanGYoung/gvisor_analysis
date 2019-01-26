#!/bin/bash

source config.sh

# Spin up
TEST_SPINUP_LIST[0]="experiments/spinup/run.sh"

# Import
TEST_IMPORT_LIST[0]="experiments/import/run.sh"

# Execute
TEST_EXECUTE_LIST[0]="experiments/getpid_throughput/test.sh
                      $GETPID_NUM_CALLS"
TEST_EXECUTE_LIST[1]="experiments/network_throughput/test.sh
                      $NETWORK_TRAILS
                      $NETWORK_URL"
TEST_EXECUTE_LIST[2]="experiments/read_throughput/test.sh
                      $READ_TRAILS
                      $READ_READ_SIZE
                      $READ_FILE"
TEST_EXECUTE_LIST[3]="experiments/write_throughput/test.sh
                      $WRITE_TRAILS
                      $WRITE_WRITE_SIZE
                      $WRITE_FILE"
# Lifecycle
TEST_LIFECYCLE_LIST[0]="experiments/thread_spinup_throughput/test.sh
                        $THREAD_SPINUP_NUM_THREADS
                        $THREAD_SPINUP_NUM_TRAILS
                        $THREAD_SPINUP_NUM_SPINUPS_PER_THREAD"

echo "Test Suite Initializing..."

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

#!/bin/bash

# Spin up
TEST_SPINUP_LIST[0]="experiments/spinup/run.sh"

# Import
TEST_IMPORT_LIST[0]="experiments/import/run.sh"

# Execute
TEST_EXECUTE_LIST[0]="experiments/getpid_throughput/test.sh"
TEST_EXECUTE_LIST[1]="experiments/network_throughput/test.sh"
TEST_EXECUTE_LIST[2]="experiments/read_throughput/test.sh"
TEST_EXECUTE_LIST[3]="experiments/write_throughput/test.sh"

# Lifecycle
TEST_LIFECYCLE_LIST[0]="experiments/thread_spinup_throughput/test.sh"

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

#!/bin/bash

#### Constants ####

TEST_EXECUTE_LIST=()
TEST_IMPORT_LIST=()
TEST_LIFECYCLE_LIST=()
TEST_SPINUP_LIST=()

TEST_FILE="test.sh"

#### Execute ####


# getpid_throughput
GETPID_FOLDER_PATH="experiments/execute/getpid_throughput/"
GETPID_APP_NAME="getpid"
GETPID_NUM_CALLS=(1000 10000 100000)


generate_cmds() {
  RUNTIME=$1

	#Getpid_throughput
	for i in ${GETPID_NUM_CALLS[@]}
	do
		TEST_EXECUTE_LIST+=("$GETPID_FOLDER_PATH$TEST_FILE $GETPID_FOLDER_PATH $GETPID_APP_NAME $RUNTIME $i")
	done

}

#!/bin/bash

#### Constants ####

TEST_EXECUTE_LIST=()

TEST_FILE="test.sh"

#### Execute ####

# getpid_throughput
GETPID_FOLDER_PATH="experiments/execute/getpid_throughput/"
GETPID_APP_NAME="getpid"
GETPID_NUM_CALLS=(100000000)
GETPID_TESTS=10

# network_throughput
NETWORK_FOLDER_PATH="experiments/execute/network_throughput/"
NETWORK_APP_NAME="net"
NETWORK_TRIALS=10
NETWORK_URL=("http://speedtest.wdc01.softlayer.com/downloads/test10.zip" "http://speedtest.wdc01.softlayer.com/downloads/test100.zip" "http://speedtest.wdc01.softlayer.com/downloads/test500.zip" "http://speedtest.wdc01.softlayer.com/downloads/test1000.zip")

# read_throughput
READ_FOLDER_PATH="experiments/execute/read_throughput/"
READ_APP_NAME="read"
READ_TRIALS=100000
READ_READ_SIZE=(10 100 1000 10000) # Product of Trials and read size must be less than 10MB
READ_FILE="./file.txt"
READ_TESTS=10

# write_throughput
WRITE_FOLDER_PATH="experiments/execute/write_throughput/"
WRITE_APP_NAME="write"
WRITE_TRIALS=100000
WRITE_WRITE_SIZE=(10 100 1000 10000)
WRITE_FILE="./file.txt"
WRITE_TESTS=10

	# Generate list of tests
generate_cmds() {
  RUNTIME=$1
	# Write throughput
	for i in ${WRITE_WRITE_SIZE[@]}
	do
		for (( j=1; j <= $WRITE_TESTS; ++j ))
		do
			TEST_EXECUTE_LIST+=("$WRITE_FOLDER_PATH$TEST_FILE $WRITE_FOLDER_PATH $WRITE_APP_NAME $RUNTIME $WRITE_TRIALS $i $WRITE_FILE")
		done
	done

	# #Getpid_throughput
	# for i in ${GETPID_NUM_CALLS[@]}
	# do
	# 	for (( j=1; j <= $GETPID_TESTS; ++j ))
	# 	do
	# 		TEST_EXECUTE_LIST+=("$GETPID_FOLDER_PATH$TEST_FILE $GETPID_FOLDER_PATH $GETPID_APP_NAME $RUNTIME $i")
	# 	done
	# done
  #
	# #Network_throughput
	# for i in ${NETWORK_URL[@]}
	# do
	# 	TEST_EXECUTE_LIST+=("$NETWORK_FOLDER_PATH$TEST_FILE $NETWORK_FOLDER_PATH $NETWORK_APP_NAME $RUNTIME $NETWORK_TRIALS $i")
	# done

	# Read_throughput
	for i in ${READ_READ_SIZE[@]}
	do
		for (( j=1; j <= $READ_TESTS; ++j ))
		do
			TEST_EXECUTE_LIST+=("$READ_FOLDER_PATH$TEST_FILE $READ_FOLDER_PATH $READ_APP_NAME $RUNTIME $READ_TRIALS $i $READ_FILE")
		done
	done
}

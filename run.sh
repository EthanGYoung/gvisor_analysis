#!/bin/bash

source config.sh

generate_cmds() {
	RUNTIME=$1

	# Spin up
	TEST_SPINUP_LIST[0]="experiments/spinup/run.sh"

	# Import
	TEST_IMPORT_LIST[0]="experiments/import/run.sh"

	# Execute
	TEST_EXECUTE_LIST[0]="$GETPID_FOLDER_PATH$(echo "test.sh")
			      	$GETPID_FOLDER_PATH
				$GETPID_APP_NAME
				$RUNTIME
				$GETPID_NUM_CALLS"
	TEST_EXECUTE_LIST[1]="$NETWORK_FOLDER_PATH$(echo "test.sh")
			      	$NETWORK_FOLDER_PATH
				$NETWORK_APP_NAME
				$RUNTIME
				$NETWORK_TRAILS
			     	$NETWORK_URL"
	TEST_EXECUTE_LIST[2]="$READ_FOLDER_PATH$(echo "test.sh")
			      	$READ_FOLDER_PATH
				$READ_APP_NAME
				$RUNTIME
				$READ_TRAILS
			      	$READ_READ_SIZE
				$READ_FILE"
	TEST_EXECUTE_LIST[3]="$WRITE_FOLDER_PATH$(echo "test.sh")
				$WRITE_FOLDER_PATH
				$WRITE_APP_NAME
				$RUNTIME
				$WRITE_TRAILS
			      	$WRITE_WRITE_SIZE
			      	$WRITE_FILE"
	# Lifecycle
	TEST_LIFECYCLE_LIST[0]="$THREAD_FOLDER_PATH$(echo "test.sh")
				$THREAD_FOLDER_PATH
				$THREAD_APP_NAME
				$RUNTIME
				$THREAD_SPINUP_NUM_THREADS
				$THREAD_SPINUP_NUM_TRAILS
				$THREAD_SPINUP_NUM_SPINUPS_PER_THREAD"
}

create_log() {
  #Get correct path to log
  LOG_PATH=$(echo $1 | cut -d' ' -f 1)
  LOG_PATH=$(pwd)$(echo "/")$(echo $LOG_PATH | rev | cut -c 8- | rev)$(echo "logs/test.log")
}

echo "Test Suite Initializing..."

echo "Copying test.sh and funcs.sh to all directories"
echo experiments/*/*/ | xargs -n 1 cp test.sh
echo experiments/*/*/ | xargs -n 1 cp funcs.sh

echo "Test Suite executing on bare metal."
generate_cmds "runsc"

TEST_LIST=( #"${TEST_SPINUP_LIST[@]}" \
            #"${TEST_IMPORT_LIST[@]}" \
            "${TEST_EXECUTE_LIST[@]}" \
            #"${TEST_LIFECYCLE_LIST[@]}" \
          )

HOME_DIR=$(pwd)

for i in "${TEST_LIST[@]}"
do
  echo "Initializing test: $i"
  
  #create_log $i
  #echo "Saving log to $LOG_PATH"
  /bin/bash $i
  #/bin/bash $i > $LOG_PATH
  cd $HOME_DIR
done

echo "Deleting test.sh and funcs.sh from all directories"
rm experiments/*/*/test.sh ; rm experiments/*/*/funcs.sh

echo "Test Suite Completed"

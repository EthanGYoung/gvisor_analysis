#!/bin/bash

source config.sh

generate_cmds() {
	RUNTIME=$1

	# Spin up
	TEST_SPINUP_LIST[0]="$C_SPINUP_FOLDER_PATH$(echo "test.sh")
							$C_SPINUP_FOLDER_PATH
							$C_SPINUP_APP_NAME
							$RUNTIME
							$C_SPINUP_NUM_TRAILS"
	TEST_SPINUP_LIST[1]="$PYTHON_SPINUP_FOLDER_PATH$(echo "test.sh")
							$PYTHON_SPINUP_FOLDER_PATH
							$PYTHON_SPINUP_APP_NAME
							$RUNTIME
							$PYTHON_SPINUP_NUM_TRAILS"

	# Import
	TEST_IMPORT_LIST[0]="$DJANGO_FOLDER_PATH$(echo "test.sh")
							$DJANGO_FOLDER_PATH
							$DJANGO_APP_NAME
							$RUNTIME
							$DJANGO_NUM_TRAILS"
	TEST_IMPORT_LIST[1]="$FLASK_FOLDER_PATH$(echo "test.sh")
							$FLASK_FOLDER_PATH
							$FLASK_APP_NAME
							$RUNTIME
							$FLASK_NUM_TRAILS"
	TEST_IMPORT_LIST[2]="$JINJA2_FOLDER_PATH$(echo "test.sh")
							$JINJA2_FOLDER_PATH
							$JINJA2_APP_NAME
							$RUNTIME
							$JINJA2_NUM_TRAILS"
	TEST_IMPORT_LIST[3]="$MATPLOTLIB_FOLDER_PATH$(echo "test.sh")
							$MATPLOTLIB_FOLDER_PATH
							$MATPLOTLIB_APP_NAME
							$RUNTIME
							$MATPLOTLIB_NUM_TRAILS"
	TEST_IMPORT_LIST[4]="$NUMPY_FOLDER_PATH$(echo "test.sh")
							$NUMPY_FOLDER_PATH
							$NUMPY_APP_NAME
							$RUNTIME
							$NUMPY_NUM_TRAILS"
	TEST_IMPORT_LIST[5]="$PIP_FOLDER_PATH$(echo "test.sh")
						$PIP_FOLDER_PATH
						$PIP_APP_NAME
						$RUNTIME
						$PIP_NUM_TRAILS"
 TEST_IMPORT_LIST[6]="$REQUESTS_FOLDER_PATH$(echo "test.sh")
						$REQUESTS_FOLDER_PATH
						$REQUESTS_APP_NAME
						$RUNTIME
						$REQUESTS_NUM_TRAILS"
 TEST_IMPORT_LIST[7]="$SETUPTOOLS_FOLDER_PATH$(echo "test.sh")
						$SETUPTOOLS_FOLDER_PATH
						$SETUPTOOLS_APP_NAME
						$RUNTIME
						$SETUPTOOLS_NUM_TRAILS"
 TEST_IMPORT_LIST[8]="$SQLALCHEMY_FOLDER_PATH$(echo "test.sh")
						$SQLALCHEMY_FOLDER_PATH
						$SQLALCHEMY_APP_NAME
						$RUNTIME
						$SQLALCHEMY_NUM_TRAILS"
 TEST_IMPORT_LIST[9]="$STANDARD_FOLDER_PATH$(echo "test.sh")
						$STANDARD_FOLDER_PATH
						$STANDARD_APP_NAME
						$RUNTIME
						$STANDARD_NUM_TRAILS"
 TEST_IMPORT_LIST[10]="$WERKZEUG_FOLDER_PATH$(echo "test.sh")
						$WERKZEUG_FOLDER_PATH
						$WERKZEUG_APP_NAME
						$RUNTIME
						$WERKZEUG_NUM_TRAILS"

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

echo experiments/import/*/ | xargs -n 1 cp experiments/import/test_config.sh
echo experiments/spinup/*/ | xargs -n 1 cp experiments/spinup/test_config.sh

echo "Test Suite executing on bare metal."
generate_cmds "runc"

TEST_LIST=( "${TEST_SPINUP_LIST[@]}" \
            "${TEST_IMPORT_LIST[@]}" \
            #"${TEST_EXECUTE_LIST[@]}" \
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
rm experiments/import/*/test_config.sh
rm experiments/spinup/*/test_config.sh


echo "Test Suite Completed"

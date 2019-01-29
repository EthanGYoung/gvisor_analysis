#!/bin/bash

if [ "$#" -ne 2 ]; then
        echo "Usage: sudo bash run.sh <RUNTIME> <Config file>"
        exit 1
fi

CONFIG=$2

source $CONFIG

get_dir_path() {
  #Get correct path to log
  DIR_PATH=$(echo $1 | cut -d' ' -f 1)
  DIR_PATH=$(pwd)$(echo "/")$(echo $DIR_PATH | rev | cut -c 8- | rev)
}

echo "Test Suite Initializing..."

echo "Copying test.sh and funcs.sh to all directories"
echo experiments/*/*/ | xargs -n 1 cp test.sh
echo experiments/*/*/ | xargs -n 1 cp funcs.sh

echo "Creating log directories and remove old logs"

mkdir "logs/"
for dir in experiments/*/; do mkdir -p -- "logs/$dir"; done
for dir in experiments/*/*/; do mkdir -p -- "logs/$dir"; done

echo "Copying test-configs to correct locations"
echo experiments/import/*/ | xargs -n 1 cp experiments/import/test_config.sh
echo experiments/spinup/*/ | xargs -n 1 cp experiments/spinup/test_config.sh

PLATFORM=$1

echo "Test Suite executing on $PLATFORM"
generate_cmds "$PLATFORM"

TEST_LIST=( "${TEST_SPINUP_LIST[@]}" \
            "${TEST_IMPORT_LIST[@]}" \
            "${TEST_EXECUTE_LIST[@]}" \
            "${TEST_LIFECYCLE_LIST[@]}" \
          )

HOME_DIR=$(pwd)

for i in "${TEST_LIST[@]}"
do
	echo "Initializing test: $i"

	get_dir_path $i

  	DIR_PATH=$(echo $DIR_PATH | cut -d'_' -f 2 | cut -c 10-)
  	#DIR_PATH=$(echo $DIR_PATH | cut -d'gvisor_analysis' -f 2)

	LOG_PATH=$(echo "logs/")$DIR_PATH$(echo "test.log")
	echo "Saving log to $LOG_PATH"
	
	/bin/bash $i >> $LOG_PATH
	
	echo ""
done

echo "Deleting test.sh and funcs.sh from all directories"
rm experiments/*/*/test.sh ; rm experiments/*/*/funcs.sh
rm experiments/import/*/test_config.sh
rm experiments/spinup/*/test_config.sh

echo "Test Suite Completed"

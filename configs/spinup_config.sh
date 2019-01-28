#!/bin/bash

#### Constants ####

TEST_SPINUP_LIST=()

TEST_FILE="test.sh"

# spinup c
C_SPINUP_FOLDER_PATH="experiments/spinup/c_spinup/"
C_SPINUP_APP_NAME="c_spinup"
C_SPINUP_NUM_TRAILS=1

# spinup python
PYTHON_FOLDER_PATH="experiments/spinup/python_spinup/"
PYTHON_SPINUP_APP_NAME="python_spinup"
PYTHON_SPINUP_NUM_TRAILS=1

	# Generate list of tests
generate_cmds() {
  RUNTIME=$1

  # spinup c
  TEST_SPINUP_LIST+=("$C_SPINUP_FOLDER_PATH$TEST_FILE $C_SPINUP_FOLDER_PATH $C_SPINUP_APP_NAME $RUNTIME $C_SPINUP_NUM_TRAILS")
  # spinup c
  TEST_SPINUP_LIST+=("$PYTHON_FOLDER_PATH$TEST_FILE $PYTHON_FOLDER_PATH $PYTHON_SPINUP_APP_NAME $RUNTIME $PYTHON_SPINUP_NUM_TRAILS")

}

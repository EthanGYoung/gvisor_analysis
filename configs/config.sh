#!/bin/bash

generate_cmds(){
  RUNTIME=$1
  #source $(pwd)"/configs/execute_config.sh"
  #generate_cmds $RUNTIME
  source $(pwd)"/configs/import_config.sh"
  generate_cmds $RUNTIME
  #source $(pwd)"/configs/lifecycle_config.sh"
  #generate_cmds $RUNTIME
  source $(pwd)"/configs/spinup_config.sh"
  generate_cmds $RUNTIME
}

#!/bin/bash

generate_cmds(){
  RUNTIME=$1
  source execute_config.sh
  generate_cmds $RUNTIME
  source import_config.sh
  generate_cmds $RUNTIME
  source lifecycle_config.sh
  generate_cmds $RUNTIME
  source spinup_config.sh
  generate_cmds $RUNTIME
}

#!/bin/bash

generate_cmds(){
  RUNTIME=$1
  
  source configs/execute_config.sh
  gen_execute_cmds $RUNTIME
  source configs/import_config.sh
  gen_import_cmds $RUNTIME
  source configs/lifecycle_config.sh
  gen_lifecycle_cmds $RUNTIME
  source configs/spinup_config.sh
  gen_spinup_cmds $RUNTIME
}

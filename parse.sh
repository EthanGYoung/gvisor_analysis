#!/bin/bash

LOG_DIRS=$(echo logs/*/*/*/)
INDICATORS=("LOG_OUTPUT" "ERROR") 
echo "Printing logs: Indicators are (${INDICATORS[@]})" 
for log in ${LOG_DIRS[@]} 
do 
        echo "Parsing log files in folder $log" 
         
        python parse.py $log ${INDICATORS[@]} 
        
        echo ""
done

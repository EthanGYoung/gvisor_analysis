#!/bin/bash
source config.sh
echo "Test Suite Initializing..."
for i in "${TEST_LIST[@]}"
do
  echo "Initializing test: $i"
  /bin/bash $i
done

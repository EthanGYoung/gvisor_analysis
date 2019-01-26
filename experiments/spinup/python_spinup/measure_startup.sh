#!/bin/bash

CREATED=$(docker inspect --format='{{.Created}}' continer_python_spinup_clean)
START=$(docker inspect --format='{{.State.StartedAt}}' continer_python_spinup_clean)

START_TIMESTAMP=$(date --date=$START +%s%N | cut -b1-13)
CREATED_TIMESTAMP=$(date --date=$CREATED +%s%N | cut -b1-13)

echo The starupt time for continer_python_spinup_clean is $(($START_TIMESTAMP-$CREATED_TIMESTAMP)) ms

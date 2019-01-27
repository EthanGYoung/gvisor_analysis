#!/bin/bash

echo "Inspecting container $1"

CREATED=$(docker inspect --format='{{.Created}}' $1)
START=$(docker inspect --format='{{.State.StartedAt}}' $1)

START_TIMESTAMP=$(date --date=$START +%s%N | cut -b1-13)
CREATED_TIMESTAMP=$(date --date=$CREATED +%s%N | cut -b1-13)

echo The startup time for $1 is $(($START_TIMESTAMP-$CREATED_TIMESTAMP)) ms

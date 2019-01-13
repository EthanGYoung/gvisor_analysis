# Experiment Description

This experiment tests the throughput for spinning up containers that can be achieved. This is important to the analysis because we if runsc is used on distributed systems (such as a lambda platform), is it usedul to know the rate at which containers can be spun up on either platform.

## Experiment Methods

1) Start X threads
2) Start timer per thread
3) Spinup Y number of containers with each thread
4) Stop timer
5) Run in different types of containers

## Current State

Finished. Future: May be best to move driver code from c to Python, since can't end program with ctr-c. 

## Notes

May be Docker processes due to killing containers that could be impacting the performance of this test.

## Author

Ethan Young

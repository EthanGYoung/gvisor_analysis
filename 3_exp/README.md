# Experiment Description

This experiment tests the throughput for spinning up containers that can be achieved. This is important to the analysis because we if runsc is used on distributed systems (such as a lambda platform), is it usedul to know the rate at which containers can be spun up on either platform.

## Experiment Methods

1) Spin up container, REPEAT( start timer, write X bytes, stop timer)
2) Run in different types of containers

# Current State

Not finished

## Notes

May be Docker processes due to killing containers that could be impacting the performance of this test.

## Author

Ethan Young

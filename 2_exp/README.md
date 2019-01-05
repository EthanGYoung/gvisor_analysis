# Experiment Description

This experiment tests the write throughput that can be achieved on bare metal, Docker (runc), Docker (runsc) with ptrace, Docker (runsc) with KVM. This is important because we would like to know the I/O cost associated with gVisor in different types of workloads.

## Experiment Methods

1) Spin up container, REPEAT( start timer, write X bytes, stop timer)
2) Run in different types of containers

# Current State

Finished. Future: May include writing on tmpfs for bare metal.

## Notes

Likely writing to only RAM since times are so fast

## Author

Ethan Young

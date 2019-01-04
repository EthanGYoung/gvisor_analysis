# Experiment Description

This experiment tests the read throughput that can be achieved on bare metal, Docker (runc), Docker (runsc) with ptrace, Docker (runsc) with KVM. This is important because we would like to know the I/O cost associated with gVisor in different types of workloads.

## Experiment Methods

1) Spin up container, REPEAT( start timer, read X bytes, stop timer)
2) Run in different types of containers

## Notes
Most likely memory being cached in OS, so will see very fast reads.

## Author

Ethan Young

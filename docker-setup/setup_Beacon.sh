#!/bin/bash

## Beacon is only provided in prebuilt forms.
## Consequently, we need to match the llvm version that built Beacon.
## However, building llvm 4 in our environment was not trivial.
## Therefore, we use the both Beacon and llvm4 as prebuilt forms,
## directed extracted from the official Beacon docker image.
## They are copied to docker by the Dockerfile.
cd /fuzzer/Beacon
cat llvm4.tar.gz* > llvm4.tar.gz
tar -zxf /fuzzer/Beacon/llvm4.tar.gz
rm /fuzzer/Beacon/llvm4.tar.gz*
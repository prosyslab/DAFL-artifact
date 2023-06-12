#!/bin/bash
git clone https://github.com/google/AFL.git AFL || exit 1
cd AFL && git checkout v2.57b || exit 1
make && cd llvm_mode && make

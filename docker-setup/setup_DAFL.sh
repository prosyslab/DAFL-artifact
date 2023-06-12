#!/bin/bash
git clone https://github.com/prosyslab/DAFL.git DAFL || exit 1
cd DAFL && git checkout DAFL || exit 1
make && cd llvm_mode && make

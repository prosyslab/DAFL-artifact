#!/bin/bash
git clone https://github.com/prosyslab/DAFL.git DAFL || exit 1
cd DAFL && make && cd llvm_mode && make

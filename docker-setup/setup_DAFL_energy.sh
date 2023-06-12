#!/bin/bash
git clone https://github.com/prosyslab/DAFL.git DAFL_energy || exit 1
cd DAFL_energy && git checkout DAFL-energy || exit 1
make && cd llvm_mode && make

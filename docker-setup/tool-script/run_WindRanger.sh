#!/bin/bash

FUZZER_NAME='WindRanger'
. $(dirname $0)/common-setup.sh

# cp *.txt
cp /benchmark/bin/WindRanger/$1-distance.txt ./distance.txt
cp /benchmark/bin/WindRanger/$1-targets.txt ./targets.txt
cp /benchmark/bin/WindRanger/$1-condition_info.txt ./condition_info.txt
  
timeout $4 /fuzzer/WindRanger/fuzz/afl-fuzz \
  $DICT_OPT -m none -d -i seed -o output $5 -- ./$1 $2

. $(dirname $0)/common-postproc.sh

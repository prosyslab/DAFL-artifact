#!/bin/bash

FUZZER_NAME='DAFL-semRel'
. $(dirname $0)/common-setup.sh

# Add '-N' for no DFG-based seed scheduling. Thus, proximity factor is returned as 1.
timeout $4 /fuzzer/DAFL/afl-fuzz \
  $DICT_OPT -m none -d -i seed -o output -N $5 -- ./$1 $2

. $(dirname $0)/common-postproc.sh

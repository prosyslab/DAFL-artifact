#!/bin/bash

FUZZER_NAME='DAFL-selIns'
. $(dirname $0)/common-setup.sh

# '-N' for no DFG-based seed scheduling.
timeout $4 /fuzzer/DAFL/afl-fuzz \
  $DICT_OPT -m none -d -N -i seed -o output $5 -- ./$1 $2

. $(dirname $0)/common-postproc.sh

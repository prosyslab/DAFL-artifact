#!/bin/bash

FUZZER_NAME='Beacon'
. $(dirname $0)/common-setup.sh

timeout $4 /fuzzer/Beacon/afl-fuzz \
  $DICT_OPT -m none -d -i seed -o output $5 -- ./$1 $2

. $(dirname $0)/common-postproc.sh

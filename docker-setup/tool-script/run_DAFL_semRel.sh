#!/bin/bash

FUZZER_NAME='DAFL-semRel'
. $(dirname $0)/common-setup.sh

timeout $4 /fuzzer/DAFL/afl-fuzz \
  $DICT_OPT -m none -d -i seed -o output $5 -- ./$1 $2

. $(dirname $0)/common-postproc.sh

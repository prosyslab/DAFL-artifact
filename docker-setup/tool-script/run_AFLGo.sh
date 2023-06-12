#!/bin/bash

FUZZER_NAME='AFLGo'
. $(dirname $0)/common-setup.sh

# Set exploitation time as 20 hours for 24 hours experiment.
# this is according to the AFLgo paper.
timeout $4 /fuzzer/AFLGo/afl-fuzz \
  $DICT_OPT -m none -d -z exp -c 20h -i seed -o output $5 -- ./$1 $2

. $(dirname $0)/common-postproc.sh

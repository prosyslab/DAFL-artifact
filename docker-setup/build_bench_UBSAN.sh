#!/bin/bash

. $(dirname $0)/build_bench_common.sh

# arg1 : Target project
# arg2~: Fuzzing targets
function build_with_ASAN() {

    for TARG in "${@:2}"; do
        cd /benchmark

        str_array=($TARG)
        export BIN_NAME=${str_array[0]}
        if  [[ $BIN_NAME == "readelf" || $BIN_NAME == "objdump-2.31.1" ]]; then
            BIT_OPT="-m32"
        else
            BIT_OPT=""
        fi

        build_target $1 "clang" "clang++" "-fsanitize=integer-divide-by-zero $BIT_OPT"

        for BUG_NAME in "${str_array[@]:1}"; do
            copy_build_result $1 $BIN_NAME $BUG_NAME "UBSAN"
        done
    done
    rm -rf RUNDIR-$1 || exit 1
}

export TOOL_NAME="UBSAN"
# Build with ASAN only
mkdir -p /benchmark/bin/UBSAN
build_with_ASAN "libming-4.7" \
    "swftophp-4.7 2016-9827 2016-9829 2016-9831 2017-9988 2017-11728 2017-11729"
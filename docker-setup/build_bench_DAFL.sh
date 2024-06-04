#!/bin/bash

. $(dirname $0)/build_bench_common.sh

# arg1 : Target project
# arg2~: Fuzzing targets
function build_with_DAFL() {
    CC="/fuzzer/DAFL/afl-clang-fast"
    CXX="/fuzzer/DAFL/afl-clang-fast++"

    for TARG in "${@:2}"; do
        cd /benchmark

        str_array=($TARG)
        BIN_NAME=${str_array[0]}
        if  [[ $BIN_NAME == "readelf" || $BIN_NAME == "objdump-2.31.1" ]]; then
            BIT_OPT="-m32"
        else
            BIT_OPT=""
        fi

        for BUG_NAME in "${str_array[@]:1}"; do
            export DAFL_SELECTIVE_COV="/benchmark/DAFL-input/inst-targ/$BIN_NAME/$BUG_NAME"
            export DAFL_DFG_SCORE="/benchmark/DAFL-input/dfg/$BIN_NAME/$BUG_NAME"
            build_target $1 $CC $CXX "-fsanitize=integer-divide-by-zero $BIT_OPT" 2>&1 | tee /benchmark/build_log/$BIN_NAME-$BUG_NAME.txt

            ### copy results
            copy_build_result $1 $BIN_NAME $BUG_NAME "DAFL"
            rm -rf RUNDIR-$1
        done
    done

}

# Build with DAFL
mkdir -p /benchmark/build_log
mkdir -p /benchmark/bin/DAFL
build_with_DAFL "jasper" \
    "imginfo patron"
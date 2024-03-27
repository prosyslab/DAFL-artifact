#!/bin/bash

. $(dirname $0)/build_bench_common.sh

# arg1 : Target project
# arg2~: Fuzzing targets
function build_with_ASAN() {

    for TARG in "${@:2}"; do
        cd /benchmark

        str_array=($TARG)
        BIN_NAME=${str_array[0]}
        if  [[ $BIN_NAME == "readelf" || $BIN_NAME == "binutils-2.31.1" ]]; then
            BIT_OPT="-m32"
        else
            BIT_OPT=""
        fi

        build_target $1 "clang" "clang++" "-fsanitize=address $BIT_OPT"

        for BUG_NAME in "${str_array[@]:1}"; do
            copy_build_result $1 $BIN_NAME $BUG_NAME "ASAN"
        done
    done
    rm -rf RUNDIR-$1 || exit 1
}

export TOOL_NAME="ASAN"
# Build with ASAN only
mkdir -p /benchmark/bin/ASAN
build_with_ASAN "libming-4.7" \
    "swftophp-4.7 2016-9827 2016-9829 2016-9831 2017-9988 2017-11728 2017-11729" &
build_with_ASAN "libming-4.7.1" \
    "swftophp-4.7.1 2017-7578" &
build_with_ASAN "libming-4.8" \
    "swftophp-4.8 2018-7868 2018-8807 2018-8962 2018-11095 2018-11225 2018-11226 2020-6628 2018-20427 2019-12982" &
build_with_ASAN "libming-4.8.1" \
    "swftophp-4.8.1 2019-9114" &
build_with_ASAN "lrzip-9de7ccb" "lrzip-9de7ccb 2017-8846" &
build_with_ASAN "lrzip-ed51e14" "lrzip-ed51e14 2018-11496" &
build_with_ASAN "binutils-2.26" \
    "cxxfilt 2016-4487 2016-4489 2016-4490 2016-4491 2016-4492 2016-6131" &
build_with_ASAN "binutils-2.28" \
    "objdump 2017-8392 2017-8396 2017-8397 2017-8398" \
    "objcopy 2017-8393 2017-8394 2017-8395" &
build_with_ASAN "binutils-2.31.1" "objdump-2.31.1 2018-17360" &
build_with_ASAN "binutils-2.27" "strip 2017-7303" &
build_with_ASAN "binutils-2.29" "nm 2017-14940" &
build_with_ASAN "libxml2-2.9.4" "xmllint 2017-5969 2017-9047 2017-9048" &
build_with_ASAN "libjpeg-1.5.90" "cjpeg-1.5.90 2018-14498" &
build_with_ASAN "libjpeg-2.0.4" "cjpeg-2.0.4 2020-13790" &

wait

build_with_ASAN "binutils-2.29" "readelf 2017-16828"
#!/bin/bash

. $(dirname $0)/build_bench_common.sh
set -x
# arg1 : Target project
# arg2 : Compiler to use for the final build.
# arg3 : Additional compiler options (e.g. LDFLAGS) for the final build.
# arg4~: fuzzing target string
function build_with_WindRanger() {

    for TARG in "${@:4}"; do
        cd /benchmark

        str_array=($TARG)
        BIN_NAME=${str_array[0]}
        if  [[ $BIN_NAME == "readelf" || $BIN_NAME == "objdump-2.31.1" ]]; then
            BIT_OPT="-m32"
        else
            BIT_OPT=""
        fi

        arr=(${BIN_NAME//-/ })
        SIMPLE_BIN_NAME=${arr[0]}

        cd /benchmark
        CC="gclang"
        CXX="gclang++"
        
        build_target $1 $CC $CXX $BIT_OPT

        cd RUNDIR-$1
        get-bc $BIN_NAME || exit 1

        if  [[ "$BIN_NAME" == *"cjpeg"* ]]; then
            build_target $1 $CC $CXX $BIT_OPT
        fi

        for BUG_NAME in "${str_array[@]:1}"; do
            mkdir output-$BIN_NAME
            cd output-$BIN_NAME
            cp ../$BIN_NAME.bc ./

            /fuzzer/WindRanger/instrument/bin/cbi --targets=/benchmark/target/line/$BIN_NAME/$BUG_NAME ./$BIN_NAME.bc
            
            ## Sanitizer may not function correctly when compiling from LLVM's bitcode
            ## https://github.com/google/sanitizers/issues/1476
            ## Thus, we manually insert sanitizer attributes to the functions with llvm module pass
            ## We omit nm, strip, and objcopy since they seem to crash differently when sanitizer attributes are inserted
            ## This fix was suggested by Liu Song (songliu@psu.edu)
            if [[ "$BIN_NAME" != "nm" && "$BIN_NAME" != "strip" && "$BIN_NAME" != "objcopy" ]]; then
                opt -load /fuzzer/WindRanger/AddSan.so -add-sanitize-address < $BIN_NAME.ci.bc > $BIN_NAME.asan.ci.bc
            else
                ## handle nm, strip, and objcopy
                cp $BIN_NAME.ci.bc $BIN_NAME.asan.ci.bc
            fi
            
            $2 $BIN_NAME.asan.ci.bc $3 -fsanitize=address $BIT_OPT -o ./$BIN_NAME-$BUG_NAME

            cp ./$BIN_NAME-$BUG_NAME /benchmark/bin/WindRanger/$BIN_NAME-$BUG_NAME || exit 1
            cp ./distance.txt /benchmark/bin/WindRanger/$BIN_NAME-$BUG_NAME-distance.txt
            cp ./targets.txt /benchmark/bin/WindRanger/$BIN_NAME-$BUG_NAME-targets.txt
            cp ./condition_info.txt /benchmark/bin/WindRanger/$BIN_NAME-$BUG_NAME-condition_info.txt
            cd ..
            rm -r output-$BIN_NAME
        done
    done

    rm -rf RUNDIR-$1 || exit 1

}

export PATH=/usr/lib/llvm-10/bin:$PATH
export PATH=/usr/lib/llvm-10/lib:$PATH
export PATH=/root/go/bin:$PATH

# Build with WindRanger
mkdir -p /benchmark/bin/WindRanger
build_with_WindRanger "libming-4.7" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-lm -lz" \
    "swftophp-4.7 2016-9827 2016-9829 2016-9831 2017-9988 2017-11728 2017-11729" &
build_with_WindRanger "libming-4.7.1" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-lm -lz" \
    "swftophp-4.7.1 2017-7578" &
build_with_WindRanger "libming-4.8" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-lm -lz" \
    "swftophp-4.8 2018-7868 2018-8807 2018-8962 2018-11095 2018-11225 2018-11226 2018-20427 2019-12982 2020-6628" &
build_with_WindRanger "libming-4.8.1" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-lm -lz" \
    "swftophp-4.8.1 2019-9114" &
build_with_WindRanger "lrzip-9de7ccb" "/fuzzer/WindRanger/fuzz/afl-clang-fast++" "-lm -lz -lpthread -llzo2 -lbz2" \
    "lrzip-9de7ccb 2017-8846" &
build_with_WindRanger "lrzip-ed51e14" "/fuzzer/WindRanger/fuzz/afl-clang-fast++" "-lm -lz -lpthread -llzo2 -lbz2" \
    "lrzip-ed51e14 2018-11496" &
build_with_WindRanger "binutils-2.26" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-ldl" \
    "cxxfilt 2016-4487 2016-4489 2016-4490 2016-4491 2016-4492 2016-6131" &
build_with_WindRanger "binutils-2.28" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-ldl" \
    "objdump 2017-8392 2017-8396 2017-8397 2017-8398" \
    "objcopy 2017-8393 2017-8394 2017-8395" &
build_with_WindRanger "binutils-2.31.1" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-ldl -fsanitize=address" \
    "objdump-2.31.1 2018-17360" &
build_with_WindRanger "binutils-2.27" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-ldl -fsanitize=address" \
    "strip 2017-7303" &
build_with_WindRanger "binutils-2.29" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-ldl -fsanitize=address" \
    "nm 2017-14940" &
build_with_WindRanger "libxml2-2.9.4" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-lm -lz" \
    "xmllint 2017-5969 2017-9047 2017-9048" &
# For libjpeg, we should also pass .a file as input, too.
build_with_WindRanger "libjpeg-1.5.90" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "../RUNDIR-libjpeg-1.5.90/libjpeg-turbo-1.5.90/libjpeg.a" \
    "cjpeg-1.5.90 2018-14498" &
build_with_WindRanger "libjpeg-2.0.4" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "../RUNDIR-libjpeg-2.0.4/libjpeg-turbo-2.0.4/libjpeg.a" \
    "cjpeg-2.0.4 2020-13790" &

wait

build_with_WindRanger "binutils-2.29" "/fuzzer/WindRanger/fuzz/afl-clang-fast" "-ldl -fsanitize=address" \
   "readelf 2017-16828"
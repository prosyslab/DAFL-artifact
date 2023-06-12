#!/bin/bash

DEFAULT_FLAGS="-g -fno-omit-frame-pointer -Wno-error"

# arg1 : build target name
# arg2 : string for CC
# arg3 : string for CXX
# arg4 : additional string for CFLAGS (optional)
function build_target() {
    # Strangely, some C programs use CXX for compiler. So set CXX* vars, too.
    export CC=$2
    export CXX=$3
    export CFLAGS="$DEFAULT_FLAGS $4"
    export CXXFLAGS="$DEFAULT_FLAGS $4"
    #while true; do
    #    /benchmark/project/build-target.sh $1 || continue
    #    break
    #done
    # Do not run in loop until our initial integration is completed.
    /benchmark/project/build-target.sh $1
}

# arg1 : project name
# arg2 : binary name
# arg3 : bug name
# arg4 : fuzzer kind
# Note that a single binary can become multiple fuzzing targets.
function copy_build_result() {
    TARG=$2-$3
    cp RUNDIR-$1/$2 /benchmark/bin/$4/$TARG || exit 1
    # If we have 'poc' or 'poc-<binname>' directory, copy it.
    if [[ -d project/$1/poc && ! -d /benchmark/poc/$2 ]]; then
        cp -r project/$1/poc /benchmark/poc/$2 || exit 1
    fi
    if [[ -d project/$1/poc-$2 && ! -d /benchmark/poc/$2 ]]; then
        cp -r project/$1/poc-$2 /benchmark/poc/$2 || exit 1
    fi
    # If we have 'seed' or 'seed-<binname>' directory, copy it.
    if [[ -d project/$1/seed-$2-$3 && ! -d /benchmark/seed/$TARG ]]; then
        cp -r project/$1/seed-$2-$3 /benchmark/seed/$TARG || exit 1
    elif [[ -d project/$1/seed-$2 && ! -d /benchmark/seed/$TARG ]]; then
        cp -r project/$1/seed-$2 /benchmark/seed/$TARG || exit 1
    elif [[ -d project/$1/seed && ! -d /benchmark/seed/$TARG ]]; then
        cp -r project/$1/seed /benchmark/seed/$TARG || exit 1
    fi
}

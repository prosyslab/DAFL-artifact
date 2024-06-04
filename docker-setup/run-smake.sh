#!/bin/bash
set -x
. $(dirname $0)/build_bench_common.sh
mkdir -p /benchmark/smake-out

export CC="clang"
export CXX="clang++"

### Program: libming-4.7
cd /benchmark
program="libming-4.7"
binaries="swftophp"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/BUILD
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r BUILD/sparrow/util/$binary /benchmark/smake-out/$binary-4.7 || exit 1
done


rm -rf /benchmark/RUNDIR*
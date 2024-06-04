#!/bin/bash
set -x
. $(dirname $0)/build_bench_common.sh
mkdir -p /benchmark/smake-out

export CC="clang"
export CXX="clang++"

### Program: libming-4.7
cd /benchmark
program="jasper-patron"
binaries="swftophp"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/jasper-patron
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r jasper-patron/sparrow/src/appl/.libs/imginfo/*.i /benchmark/smake-out/jasper-patron || exit 1
done


rm -rf /benchmark/RUNDIR*
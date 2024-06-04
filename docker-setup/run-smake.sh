#!/bin/bash
set -x
. $(dirname $0)/build_bench_common.sh
mkdir -p /benchmark/smake-out

export CC="clang"
export CXX="clang++"

### Program: libming-4.7
cd /benchmark
program="jasper"
binaries="imginfo"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/jasper
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
mkdir -p /benchmark/smake-out/imginfo

find jasper/sparrow/src/libjasper/*/.libs -name "*.i" -exec cp {} /benchmark/smake-out/imginfo \;
cp jasper/sparrow/src/appl/imginfo.o.i /benchmark/smake-out/imginfo


rm -rf /benchmark/RUNDIR*
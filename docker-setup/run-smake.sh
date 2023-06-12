#!/bin/bash
set -x
. $(dirname $0)/build_bench_common.sh
mkdir -p /benchmark/smake-out

export CC="clang"
export CXX="clang++"
export CMAKE_EXPORT_COMPILE_COMMANDS=1

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


### Program: libming-4.7.1
cd /benchmark
program="libming-4.7.1"
binaries="swftophp"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/BUILD
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r BUILD/sparrow/util/$binary /benchmark/smake-out/$binary-4.7.1 || exit 1
done


### Program: libming-4.8
cd /benchmark
program="libming-4.8"
binaries="swftophp"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/BUILD
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r BUILD/sparrow/util/$binary /benchmark/smake-out/$binary-4.8 || exit 1
done


### Program: libming-4.8.1
cd /benchmark
program="libming-4.8.1"
binaries="swftophp"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/BUILD
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r BUILD/sparrow/util/$binary /benchmark/smake-out/$binary-4.8.1 || exit 1
done


### Program: lrzip-9de7ccb
cd /benchmark
program="lrzip-9de7ccb"
binaries="lrzip"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/BUILD
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r BUILD/sparrow/$binary /benchmark/smake-out/$program || exit 1
done
cd /benchmark
rm -rf /benchmark/RUNDIR*


### Program: lrzip-ed51e14
cd /benchmark
program="lrzip-ed51e14"
binaries="lrzip"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/BUILD
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r BUILD/sparrow/$binary /benchmark/smake-out/$binary-ed51e14 || exit 1
done


### Program: binutils-2.26
cd /benchmark
program="binutils-2.26"
binaries="cxxfilt"
CC=clang CXX=clang++ CFLAGS="-Wno-error" /benchmark/project/build-target.sh $program
cd /benchmark/RUNDIR-$program/$program
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r $program/sparrow/binutils/$binary /benchmark/smake-out/$binary || exit 1
done


### Program: binutils-2.28
cd /benchmark
program="binutils-2.28"
binaries="objdump objcopy"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/$program
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r $program/sparrow/binutils/$binary /benchmark/smake-out/$binary || exit 1
done


### Program: binutils-2.27
cd /benchmark
program="binutils-2.27"
binaries="strip"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/$program
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r $program/sparrow/binutils/$binary-new /benchmark/smake-out/$binary || exit 1
done
cd /benchmark
rm -rf /benchmark/RUNDIR*


### Program: binutils-2.29
program="binutils-2.29"
binaries="readelf"
build_target $program $CC $CXX "-m32"
cd /benchmark/RUNDIR-$program/$program
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program

for binary in $binaries; do
    cp -r $program/sparrow/binutils/$binary /benchmark/smake-out/$binary || exit 1
done
cd /benchmark
rm -rf /benchmark/RUNDIR*


### Program: binutils-2.29
program="binutils-2.29"
binaries="nm"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/$program
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r $program/sparrow/binutils/$binary-new /benchmark/smake-out/$binary || exit 1
done
cd /benchmark
rm -rf /benchmark/RUNDIR*


### Program: binutils-2.31.1
cd /benchmark
program="binutils-2.31.1"
binaries="objdump"
build_target $program $CC $CXX "-m32"
cd /benchmark/RUNDIR-$program/$program
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r binutils-2.31.1/sparrow/binutils/$binary /benchmark/smake-out/$binary-2.31.1 || exit 1
done
cd /benchmark
rm -rf /benchmark/RUNDIR*


### Program: libxml2-2.9.4
cd /benchmark
program="libxml2-2.9.4"
binaries="xmllint"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/$program
make clean
yes | /smake/smake --init
/smake/smake -j 1
cd /benchmark/RUNDIR-$program
for binary in $binaries; do
    cp -r $program/sparrow/xmllint /benchmark/smake-out/$binary || exit 1
done


### Program: libjpeg-1.5.90
cd /benchmark
program="libjpeg-1.5.90"
binaries="cjpeg"

build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/libjpeg-turbo-1.5.90
make clean
/smake/scmake --cmake-out tempo
cd /benchmark/RUNDIR-$program

d_files="jcstest.i jpegtran.i rdjpgcom.i tjbench.i tjexample.i tjunittest.i wrjpgcom.i djpeg.i"
for binary in $binaries; do
    mkdir /benchmark/smake-out/$binary-1.5.90
    cp libjpeg-turbo-1.5.90/sparrow/*.i /benchmark/smake-out/$binary-1.5.90/ || exit 1
    for d_file in $d_files; do
        rm /benchmark/smake-out/$binary-1.5.90/$d_file || exit 1
    done
done

cd /benchmark/smake-out
patch -p0 < /benchmark/patches/cjpeg-1.5.90.patch

### Program: libjpeg-2.0.4
cd /benchmark
program="libjpeg-2.0.4"
binaries="cjpeg"
build_target $program $CC $CXX " "
cd /benchmark/RUNDIR-$program/libjpeg-turbo-2.0.4
make clean
/smake/scmake --cmake-out tempo
cd /benchmark/RUNDIR-$program

d_files="jcstest.i jpegtran.i rdjpgcom.i tjbench.i tjexample.i tjunittest.i wrjpgcom.i djpeg.i"
for binary in $binaries; do
    mkdir /benchmark/smake-out/$binary-2.0.4
    cp libjpeg-turbo-2.0.4/sparrow/*.i /benchmark/smake-out/$binary-2.0.4 || exit 1
    for d_file in $d_files; do
        rm /benchmark/smake-out/$binary-2.0.4/$d_file || exit 1
    done
done

cd /benchmark/smake-out
patch -p0 < /benchmark/patches/cjpeg-2.0.4.patch

rm -rf /benchmark/RUNDIR*
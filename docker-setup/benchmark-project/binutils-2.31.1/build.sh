#!/bin/bash
URL="http://ftp.gnu.org/gnu/binutils/binutils-2.31.1.tar.gz"
DIRNAME="binutils-2.31.1"
ARCHIVE=$DIRNAME".tar.gz"
CONFIG_OPTIONS="--build=i686-linux --disable-shared --disable-gdb \
                 --disable-libdecnumber --disable-readline \
                 --disable-sim --disable-ld"

wget $URL -O $ARCHIVE
rm -rf $DIRNAME
tar -xzf $ARCHIVE || exit 1
cd $DIRNAME
./configure $CONFIG_OPTIONS || exit 1
## Parallel building according to https://github.com/aflgo/aflgo/issues/59
## Altohough an issue with parallel building is observed in libxml (https://github.com/aflgo/aflgo/issues/41), 
## We have not yet encountered a problem with binutils.
make -j || exit 1
cd ../
cp $DIRNAME/binutils/objdump ./objdump-2.31.1 || exit 1

#!/bin/bash
URL="https://github.com/spearo2/jasper_mirror"
DIRNAME="jasper-patron"
CONFIG_OPTIONS="--disable-shared --disable-gdb \
                 --disable-libdecnumber --disable-readline \
                 --disable-sim --disable-ld"

rm -rf $DIRNAME
git clone https://github.com/spearo2/jasper_mirror $DIRNAME
cd $DIRNAME
./configure $CONFIG_OPTIONS || exit 1
make -j || exit 1
cd ../
cp $DIRNAME/src/appl/imginfo ./jasper-patron || exit 1

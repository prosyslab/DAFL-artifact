#!/bin/bash

URL="https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/1.5.90.zip"
DIRNAME="libjpeg-turbo-1.5.90"
ARCHIVE=$DIRNAME".zip"

wget $URL -O $ARCHIVE
rm -rf $DIRNAME
unzip $ARCHIVE || exit 1
cd $DIRNAME
cmake -G"Unix Makefiles" || exit 1
make || exit 1
cd ../
cp $DIRNAME/cjpeg-static ./cjpeg-1.5.90 || exit 1

#!/bin/bash

URL="https://github.com/GNOME/libxml2/archive/refs/tags/v2.9.4.zip"
DIRNAME="libxml2-2.9.4"
ARCHIVE=$DIRNAME".zip"

wget $URL -O $ARCHIVE
rm -rf $DIRNAME
unzip $ARCHIVE || exit 1
cd $DIRNAME
./autogen.sh --disable-shared || exit 1
make || exit 1
cd ../
cp $DIRNAME/xmllint ./xmllint || exit 1

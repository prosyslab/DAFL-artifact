#!/bin/bash

build_lib() {
  rm -rf BUILD
  cp -rf SRC BUILD
  (cd BUILD && ./autogen.sh && ./configure --disable-shared --disable-freetype && make)
}
GIT_URL="https://github.com/libming/libming.git"
TAG_NAME="6dff24bc2543c55f277662144d0cec97e4a6d0c1"
RELEVANT_BINARIES="swftophp"

[ ! -e SRC ] && git clone $GIT_URL SRC
cd SRC
git checkout $TAG_NAME
cd ..

build_lib

for binary in $RELEVANT_BINARIES; do
  cp BUILD/util/$binary ./$binary-4.7.1
done

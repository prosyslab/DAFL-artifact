#!/bin/bash

# ToDo
build_lib() {
  rm -rf BUILD
  cp -rf SRC BUILD
  (cd BUILD && ./autogen.sh && ./configure && make)
}
GIT_URL="https://github.com/ckolivas/lrzip.git"
VERSION="ed51e14"
RELEVANT_BINARIES="lrzip"

[ ! -e SRC ] && git clone $GIT_URL SRC
cd SRC
git reset --hard $VERSION
cd ..

build_lib

for binary in $RELEVANT_BINARIES; do
  cp BUILD/$binary ./$binary-ed51e14 || exit 1
done


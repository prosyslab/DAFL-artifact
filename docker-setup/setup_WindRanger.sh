#!/bin/bash

# unzip WindRanger
cd /fuzzer
tar -xzf /fuzzer/windranger.tar.gz
rm /fuzzer/windranger.tar.gz
mv windranger WindRanger

## install required llvm
cd /fuzzer/WindRanger

sudo apt-get update && sudo apt-get install -yy clang-10 llvm-10-dev

## install wclang and gclang
if ! [ -x "$(command -v wllvm)"  ]; then
    pip3 install --upgrade pip==9.0.3
    pip3 install wllvm
    export LLVM_COMPILER=clang
fi
if ! [ -x "$(command -v gclang)"  ]; then
    rm -rf /usr/bin/go
    wget https://dl.google.com/go/go1.17.1.linux-amd64.tar.gz
    tar -xvf go1.17.1.linux-amd64.tar.gz
    mv go go_install
    export GOROOT=/fuzzer/WindRanger/go_install
    mv go_install/bin/go /usr/bin
    
    mkdir /root/go
    go get github.com/SRI-CSL/gllvm/cmd/...
    export PATH=/root/go/bin:$PATH
fi

## Build llvm module pass to insert ASAN atributes to all functions.
export PATH=/usr/lib/llvm-10/bin:$PATH
export PATH=/usr/lib/llvm-10/lib:$PATH

cd /fuzzer/WindRanger
mv /fuzzer/AddSan.cc ./
clang++ -shared -o AddSan.so AddSan.cc `llvm-config --cxxflags`
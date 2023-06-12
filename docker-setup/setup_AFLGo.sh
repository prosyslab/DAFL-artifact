#!/bin/bash
git clone https://github.com/aflgo/aflgo.git AFLGo
cd AFLGo
git checkout b170fad54396f376160befd87adbba28b27c15d9
apt-get -y update
apt-get -y install python3 python3-dev python3-pip libboost-all-dev ninja-build --no-install-recommends
pip3 install --upgrade pip
pip3 install networkx==2.5 pydot pydotplus
make clean all && cd llvm_mode && make clean all && cd ../distance_calculator && cmake -GNinja ./ && cmake --build ./

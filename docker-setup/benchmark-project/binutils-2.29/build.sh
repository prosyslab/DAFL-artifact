#!/bin/bash
URL="http://ftp.gnu.org/gnu/binutils/binutils-2.29.tar.gz"
DIRNAME="binutils-2.29"
ARCHIVE=$DIRNAME".tar.gz"
CONFIG_OPTIONS="--disable-shared --disable-gdb \
                 --disable-libdecnumber --disable-readline \
                 --disable-sim --disable-ld"

wget $URL -O $ARCHIVE
rm -rf $DIRNAME
tar -xzf $ARCHIVE || exit 1
cd $DIRNAME
./configure $CONFIG_OPTIONS || exit 1
## Insert prints in nm in order to catch memory over consumption that does not crash with ASAN
if [[ $BIN_NAME == "nm" && $TOOL_NAME == "ASAN" ]]; then
    sed -i '8203 s/^.*$/fprintf(stderr, \"@@@ start\\n\");&/' bfd/elf.c
    sed -i '8206 s/^.*$/fprintf(stderr, \"@@@ end\\n\");&/' bfd/elf.c
fi
## Parallel building according to https://github.com/aflgo/aflgo/issues/59
## Altohough an issue with parallel building is observed in libxml (https://github.com/aflgo/aflgo/issues/41), 
## We have not yet encountered a problem with binutils.
make -j || exit 1
cd ../
cp $DIRNAME/binutils/nm-new ./nm || exit 1
cp $DIRNAME/binutils/readelf ./readelf || exit 1

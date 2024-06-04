FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

# (Temporary: replace URL for fast download during development)
RUN sed -i 's/archive.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list

ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -yy libc6-dev binutils libgcc-9-dev
RUN apt-get install -yy \
      wget apt-transport-https git unzip \
      build-essential libtool libtool-bin gdb \
      automake autoconf bison flex python python3 sudo vim

# Copied from OSS-FUZZ
ENV OUT=/out
ENV SRC=/src
ENV WORK=/work
ENV PATH="$PATH:/out"
RUN mkdir -p $OUT $SRC $WORK
ENV CMAKE_VERSION 3.21.1
RUN wget https://github.com/Kitware/CMake/releases/download/v$CMAKE_VERSION/cmake-$CMAKE_VERSION-Linux-x86_64.sh && \
    chmod +x cmake-$CMAKE_VERSION-Linux-x86_64.sh && \
    ./cmake-$CMAKE_VERSION-Linux-x86_64.sh --skip-license --prefix="/usr/local" && \
    rm cmake-$CMAKE_VERSION-Linux-x86_64.sh && \
    rm -rf /usr/local/doc/cmake /usr/local/bin/cmake-gui
COPY docker-setup/checkout_build_install_llvm.sh /root/
RUN /root/checkout_build_install_llvm.sh
RUN rm /root/checkout_build_install_llvm.sh

# Install packages needed for fuzzers and benchmark
RUN apt-get update && \
    apt-get install -yy \
      # Several packages get uninstalled after LLVM setup.
      git build-essential bc \
      # For ParmeSan
      golang \
      # For Beacon
      libncurses5 \
      # For libming
      libfreetype6 libfreetype6-dev \
      # For libxml
      python-dev \
      # For libjpeg
      nasm \
      # For lrzip
      libbz2-dev liblzo2-dev \
      # For 32bit binaries
      gcc-multilib

# Create a fuzzer directory and setup fuzzers there.
RUN mkdir /fuzzer
WORKDIR /fuzzer

# Create a benchmark directory and start working there.
RUN mkdir -p /benchmark/bin && \
    mkdir -p /benchmark/seed && \
    mkdir -p /benchmark/poc
COPY docker-setup/seed/empty /benchmark/seed/empty
WORKDIR /benchmark

# To use ASAN during the benchmark build, these option are needed.
ENV ASAN_OPTIONS=allocator_may_return_null=1,detect_leaks=0

# Build benchmark with AFL/AFLGo.
COPY docker-setup/benchmark-project /benchmark/project
COPY docker-setup/build_bench_common.sh /benchmark/build_bench_common.sh
COPY docker-setup/build_bench_ASAN.sh /benchmark/build_bench_ASAN.sh
RUN ./build_bench_ASAN.sh

COPY docker-setup/build_bench_UBSAN.sh /benchmark/build_bench_UBSAN.sh
RUN ./build_bench_UBSAN.sh


# Run smake on bechmarks to prepare input for sparrow
COPY docker-setup/patches /benchmark/patches
COPY smake/ /smake
COPY docker-setup/run-smake.sh /benchmark/run-smake.sh
RUN /benchmark/run-smake.sh
RUN rm /benchmark/run-smake.sh

# Setup Sparrow
COPY docker-setup/setup_Sparrow.sh /setup_Sparrow.sh
RUN /setup_Sparrow.sh
RUN rm /setup_Sparrow.sh

# Analyze benchmark with Sparrow.
RUN mkdir /benchmark/scripts
COPY scripts/benchmark.py /benchmark/scripts
COPY scripts/common.py /benchmark/scripts
COPY scripts/triage.py /benchmark/scripts
COPY scripts/run_sparrow.py /benchmark/scripts
RUN python3 /benchmark/scripts/run_sparrow.py all thin
RUN python3 /benchmark/scripts/run_sparrow.py all naive

# Setup DAFL.
WORKDIR /fuzzer
COPY docker-setup/setup_DAFL.sh /fuzzer/setup_DAFL.sh
RUN ./setup_DAFL.sh

# Build benchmarks with DAFL.
WORKDIR /benchmark
COPY docker-setup/build_bench_DAFL.sh /benchmark/build_bench_DAFL.sh
RUN ./build_bench_DAFL.sh

# Build DAFL with no ASAN options to compare with Beacon
# COPY docker-setup/build_bench_DAFL_noasan.sh /benchmark/build_bench_DAFL_noasan.sh
# RUN ./build_bench_DAFL_noasan.sh

# Build benchmarks with DAFL_select, DAFL_schedule, and DAFL_naive.
COPY docker-setup/build_bench_DAFL_naive.sh /benchmark/build_bench_DAFL_naive.sh
RUN ./build_bench_DAFL_naive.sh


# Copy script for debugging.
COPY docker-setup/parse_build_log.py /benchmark/

# Copy tool running scripts.
COPY docker-setup/tool-script /tool-script

# Reset the working directory to top-level directory.
WORKDIR /
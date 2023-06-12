1. Finds a [CVE-2017-8846](https://github.com/ckolivas/lrzip/issues/71), a 1-byte-read-heap-use-after-free bug
in [lrzip -t](https://github.com/ckolivas/lrzip), reproducer provided.

```
==4026==ERROR: AddressSanitizer: heap-use-after-free on address 0x62100000dd00 at pc 0x0000004bccc5 bp 0x7ffcf3b4d9f0 sp 0x7ffcf3b4d1a0
READ of size 1 at 0x62100000dd00 thread T0
    #0 0x4bccc4 in __asan_memcpy /tmp/portage/sys-devel/llvm-3.9.1-r1/work/llvm-3.9.1.src/projects/compiler-rt/lib/asan/asan_interceptors.cc:413
    #1 0x53cff6 in read_stream /tmp/portage/app-arch/lrzip-0.631/work/lrzip-0.631/stream.c:1747:4
    #2 0x5307fc in read_vchars /tmp/portage/app-arch/lrzip-0.631/work/lrzip-0.631/runzip.c:79:6
    #3 0x5307fc in unzip_match /tmp/portage/app-arch/lrzip-0.631/work/lrzip-0.631/runzip.c:208
    #4 0x5307fc in runzip_chunk /tmp/portage/app-arch/lrzip-0.631/work/lrzip-0.631/runzip.c:329
    #5 0x5307fc in runzip_fd /tmp/portage/app-arch/lrzip-0.631/work/lrzip-0.631/runzip.c:382
    #6 0x519b41 in decompress_file /tmp/portage/app-arch/lrzip-0.631/work/lrzip-0.631/lrzip.c:826:6
    #7 0x511074 in main /tmp/portage/app-arch/lrzip-0.631/work/lrzip-0.631/main.c:669:4
    #8 0x7f743a5d278f in __libc_start_main /tmp/portage/sys-libs/glibc-2.23-r3/work/glibc-2.23/csu/../csu/libc-start.c:289
    #9 0x41abf8 in _init (/usr/bin/lrzip+0x41abf8)

```

Created the initial seed file by compressing an empty file with 'lrzip'. This
was recommended by the authors of Beacon.

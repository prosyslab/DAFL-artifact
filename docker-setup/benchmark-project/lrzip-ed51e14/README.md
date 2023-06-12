1. Finds a [CVE-2018-11496](https://github.com/ckolivas/lrzip/issues/96), a heap-use-after-free bug
in [lrzip -t](https://github.com/ckolivas/lrzip), reproducer provided.

```
READ of size 1 at 0x60200000eef0 thread T0
    #0 0x7f5752d26934 in __asan_memcpy (/usr/lib/gcc/x86_64-linux-gnu/5/libasan.so+0x8c934)
    #1 0x414655 in memcpy /usr/include/x86_64-linux-gnu/bits/string3.h:53
    #2 0x414655 in read_stream /opt/csn/lrzip/stream.c:1756
    #3 0x40ee8c in read_vchars /opt/csn/lrzip/runzip.c:79
    #4 0x40ee8c in read_header /opt/csn/lrzip/runzip.c:147
    #5 0x40ee8c in runzip_chunk /opt/csn/lrzip/runzip.c:316
    #6 0x40ee8c in runzip_fd /opt/csn/lrzip/runzip.c:384
    #7 0x407db9 in decompress_file /opt/csn/lrzip/lrzip.c:838
    #8 0x403a74 in main /opt/csn/lrzip/main.c:675
    #9 0x7f57515e082f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #10 0x404888 in _start (/opt/csn/lrzip/lrzip+0x404888)

```

Created the initial seed file by compressing an empty file with 'lrzip'. This
was recommended by the authors of Beacon.

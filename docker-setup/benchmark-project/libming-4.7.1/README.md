1. Finds a [CVE-2016-9827](https://blogs.gentoo.org/ago/2016/12/01/libming-listswf-heap-based-buffer-overflow-in-_iprintf-outputtxt-c/), a 2-byte-read-heap-buffer-overflow bug
in [listswf](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
==3132==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000eff1 at pc 0x000000499d10 bp 0x7ffc34a55e10 sp 0x7ffc34a555c0                                                       
READ of size 2 at 0x60200000eff1 thread T0                                                                                                                                                     
    #0 0x499d0f in printf_common sanitizer_common/sanitizer_common_interceptors_format.inc:545       
    #1 0x499a9d in printf_common sanitizer_common/sanitizer_common_interceptors_format.inc:545       
    #2 0x49abfa in __interceptor_vfprintf /sanitizer_common/sanitizer_common_interceptors.inc:1321    
    #3 0x509dd7 in vprintf /usr/include/bits/stdio.h:38:10                                                                                                                                     
    #4 0x509dd7 in _iprintf ming-0_4_7/util/outputtxt.c:144                                                                                            
    #5 0x51f1f5 in outputSWF_PROTECT ming-0_4_7/util/outputtxt.c:1873:5                                                                                
    #6 0x51c35b in outputBlock ming-0_4_7/util/outputtxt.c:2933:4                                                                                      
    #7 0x527e83 in readMovie ming-0_4_7/util/main.c:277:4                                                                                              
    #8 0x527e83 in main ming-0_4_7/util/main.c:350                                                                                                     
    #9 0x7f0f1ff6861f in __libc_start_main /var/tmp/portage/sys-libs/glibc-2.22-r4/work/glibc-2.22/csu/libc-start.c:289                                                                        
    #10 0x419b38 in _init (/usr/bin/listswf+0x419b38)
```


2. Finds a [CVE-2016-9829](https://blogs.gentoo.org/ago/2016/12/01/libming-listswf-heap-based-buffer-overflow-in-parseswf_definefont-parser-c/), a 2-byte-write-heap-buffer-overflow bug
in [listswf](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
==634==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000efb0 at pc 0x00000058582e bp 0x7fff1ed6df60 sp 0x7fff1ed6df58
WRITE of size 2 at 0x60200000efb0 thread T0
    #0 0x58582d in parseSWF_DEFINEFONT ming-0_4_7/util/parser.c:1656:29
    #1 0x5302cb in blockParse ming-0_4_7/util/blocktypes.c:145:14
    #2 0x527d4f in readMovie ming-0_4_7/util/main.c:265:11
    #3 0x527d4f in main ming-0_4_7/util/main.c:350
    #4 0x7fad6007961f in __libc_start_main /var/tmp/portage/sys-libs/glibc-2.22-r4/work/glibc-2.22/csu/libc-start.c:289
    #5 0x419b38 in _init (/usr/bin/listswf+0x419b38)
```

3. Finds a [CVE-2016-9831](https://blogs.gentoo.org/ago/2016/12/01/libming-listswf-heap-based-buffer-overflow-in-parseswf_rgba-parser-c/), a 1-byte-write-heap-buffer-overflow bug
in [listswf](https://github.com/libming/libming), reproducer
provided.

Time to find: TBD
```
==31250==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x62400000df10 at pc 0x00000057f342 bp 0x7ffe24b21ef0 sp 0x7ffe24b21ee8
WRITE of size 1 at 0x62400000df10 thread T0
    #0 0x57f341 in parseSWF_RGBA ming-0_4_7/util/parser.c:66:12
    #1 0x57f341 in parseSWF_MORPHGRADIENTRECORD ming-0_4_7/util/parser.c:746
    #2 0x57f341 in parseSWF_MORPHGRADIENT ming-0_4_7/util/parser.c:761
    #3 0x57e25a in parseSWF_MORPHFILLSTYLE ming-0_4_7/util/parser.c:777:7
    #4 0x58b9b8 in parseSWF_MORPHFILLSTYLES ming-0_4_7/util/parser.c:804:7
    #5 0x58b9b8 in parseSWF_DEFINEMORPHSHAPE ming-0_4_7/util/parser.c:2098
    #6 0x5302cb in blockParse ming-0_4_7/util/blocktypes.c:145:14
    #7 0x527d4f in readMovie ming-0_4_7/util/main.c:265:11
    #8 0x527d4f in main ming-0_4_7/util/main.c:350
    #9 0x7f39cc7da61f in __libc_start_main /var/tmp/portage/sys-libs/glibc-2.22-r4/work/glibc-2.22/csu/libc-start.c:289
    #10 0x419b38 in _init (/usr/bin/listswf+0x419b38)
```

4. Finds a [CVE-2017-7578](https://github.com/libming/libming/issues/68), a 1-byte-write-heap-buffer-overflow bug
in [listswf](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
==179946==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x62e00000b298 at pc 0x0000005b1be8 bp 0x7ffc849e8990 sp 0x7ffc849e8988
WRITE of size 1 at 0x62e00000b298 thread T0
    #0 0x5b1be7 in parseSWF_RGBA libming/util/parser.c:68:14
    #1 0x5f004a in parseSWF_MORPHGRADIENTRECORD libming/util/parser.c:771:3
    #2 0x5f0c1f in parseSWF_MORPHGRADIENT libming/util/parser.c:786:5
    #3 0x5ee190 in parseSWF_MORPHFILLSTYLE libming/util/parser.c:802:7
    #4 0x5f1bbe in parseSWF_MORPHFILLSTYLES libming/util/parser.c:829:7
    #5 0x634ee5 in parseSWF_DEFINEMORPHSHAPE libming/util/parser.c:2185:3
    #6 0x543923 in blockParse libming/util/blocktypes.c:145:14
    #7 0x52b2a9 in readMovie libming/util/main.c:265:11
    #8 0x528f82 in main libming/util/main.c:350:2
    #9 0x7ff0c21cdf44 in __libc_start_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287
    #10 0x4bdf5c in _start (libming/util/listswf+0x4bdf5c)

```

5. Finds a [CVE-2017-9988](https://github.com/libming/libming/issues/85), a heap-buffer-overflow bug
in [listswf](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
#0 parseABC_NS_SET_INFO (f=, nsset=,f=) at parser.c:3083
#1 parseABC_CONSTANT_POOL (cpool=0x676258, f=0x676010) at parser.c:3191
#2 0x0000000000454d14 in parseABC_FILE (abcFile=0x676250, f=0x676010) at parser.c:3426
#3 0x00000000004558b4 in parseSWF_DOABC (f=0x676010, length=0) at parser.c:3481
#4 0x0000000000416672 in blockParse (f=0x676010, length=0, header=) at blocktypes.c:145
#5 0x0000000000411f79 in readMovie (f=0x676010) at main.c:265
#6 main (argc=, argv=) at main.c:350
```

6. Finds a [CVE-2017-11728](https://github.com/libming/libming/issues/82), a 1-byte-write-read-buffer-overflow bug
in [swftocxx](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
heap-buffer-overflow on address 0x612000000170 at pc 0x000000555cee bp 0x7ffcc35fb940 sp 0x7ffcc35fb938
READ of size 1 at 0x612000000170 thread T0
    #0 0x555ced in OpCode libming-master/util/decompile.c:868:37
    #1 0x555ced in decompileSETMEMBER libming-master/util/decompile.c:1699
    #2 0x555ced in decompileAction libming-master/util/decompile.c:3202
    #3 0x5875eb in decompileActions libming-master/util/decompile.c:3401:6
    #4 0x5875eb in decompile5Action libming-master/util/decompile.c:3423
    #5 0x52a0c5 in outputSWF_DOACTION libming-master/util/outputscript.c:1548:29
    #6 0x531311 in readMovie libming-master/util/main.c:277:4
    #7 0x531311 in main libming-master/util/main.c:350
    #8 0x7fa41f1c5b34 in __libc_start_main /usr/src/debug/glibc-2.17-c758a686/csu/../csu/libc-start.c:274
    #9 0x41ae7b in _start (libming-afl-build/bin/swftocxx+0x41ae7b)

```

7. Finds a [CVE-2017-11729](https://github.com/libming/libming/issues/79), a 1-byte-write-read-buffer-overflow bug
in [swftocxx](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
READ of size 1 at 0x6120000005f0 thread T0
    #0 0x56035c in OpCode libming-master/util/decompile.c:868:37
    #1 0x56035c in decompileINCR_DECR libming-master/util/decompile.c:1440
    #2 0x537f24 in decompileAction libming-master/util/decompile.c:3222:10
    #3 0x5875eb in decompileActions libming-master/util/decompile.c:3401:6
    #4 0x5875eb in decompile5Action libming-master/util/decompile.c:3423
    #5 0x52a0c5 in outputSWF_DOACTION libming-master/util/outputscript.c:1548:29
    #6 0x531311 in readMovie libming-master/util/main.c:277:4
    #7 0x531311 in main libming-master/util/main.c:350
    #8 0x7ffb27480b34 in __libc_start_main /usr/src/debug/glibc-2.17-c758a686/csu/../csu/libc-start.c:274
    #9 0x41ae7b in _start (libming-afl-build/bin/swftocxx+0x41ae7b)

```






Finds a [CVE-](), a  bug
in [listswf](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```

```



1. Finds a [CVE-2018-7868](https://github.com/libming/libming/issues/113), a 8-byte-read-heap-buffer-overflow bug
in [swftocxx](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
==50170==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60b00000b780 at pc 0x0000004113e6 bp 0x7ffcbc1d1ea0 sp 0x7ffcbc1d1e90
READ of size 8 at 0x60b00000b780 thread T0
    #0 0x4113e5 in getName /root/libming-asan/util/decompile.c:398
    #1 0x41620b in decompileGETMEMBER /root/libming-asan/util/decompile.c:1635
    #2 0x41e5b9 in decompileAction /root/libming-asan/util/decompile.c:3216
    #3 0x41eba0 in decompileActions /root/libming-asan/util/decompile.c:3419
    #4 0x41c727 in decompileDEFINEFUNCTION /root/libming-asan/util/decompile.c:2759
    #5 0x41e7b8 in decompileAction /root/libming-asan/util/decompile.c:3279
    #6 0x41eba0 in decompileActions /root/libming-asan/util/decompile.c:3419
    #7 0x41b07e in decompileIF /root/libming-asan/util/decompile.c:2581
    #8 0x41e715 in decompileAction /root/libming-asan/util/decompile.c:3260
    #9 0x41eba0 in decompileActions /root/libming-asan/util/decompile.c:3419
    #10 0x41eccd in decompile5Action /root/libming-asan/util/decompile.c:3441
    #11 0x40d221 in outputSWF_INITACTION /root/libming-asan/util/outputscript.c:1860
    #12 0x40e331 in outputBlock /root/libming-asan/util/outputscript.c:2083
    #13 0x40f3d9 in readMovie /root/libming-asan/util/main.c:286
    #14 0x40fb0e in main /root/libming-asan/util/main.c:359
    #15 0x7fae9b56982f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #16 0x401b58 in _start (/usr/local/libming-asan/bin/swftocxx+0x401b58)

```

2. Finds a [CVE-2018-8807](https://github.com/libming/libming/issues/129), a 8-byte-read-heap-buffer-overflow bug
in [swftophp](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
==141122==ERROR: AddressSanitizer: heap-use-after-free on address 0x603000000070 at pc 0x00000041eed4 bp 0x7ffe2359b230 sp 0x7ffe2359b228 
READ of size 8 at 0x603000000070 thread T0 
    #0 0x41eed3 in getString /u/test/product/libming/master/src/util/decompile.c:349 
    #1 0x4221ee in newVar_N /u/test/product/libming/master/src/util/decompile.c:661 
    #2 0x4318e6 in decompileCALLFUNCTION /u/test/product/libming/master/src/util/decompile.c:2895 
    #3 0x4318e6 in decompileAction /u/test/product/libming/master/src/util/decompile.c:3282 
    #4 0x44af74 in decompileActions /u/test/product/libming/master/src/util/decompile.c:3419 
    #5 0x44af74 in decompile5Action /u/test/product/libming/master/src/util/decompile.c:3441 
    #6 0x411740 in outputSWF_DOACTION /u/test/product/libming/master/src/util/outputscript.c:1551 
    #7 0x402b69 in readMovie /u/test/product/libming/master/src/util/main.c:286 
    #8 0x402b69 in main /u/test/product/libming/master/src/util/main.c:359 
    #9 0x7fd2c9a85c04 in __libc_start_main (/lib64/libc.so.6+0x21c04) 
    #10 0x4043d3 (/home/test/product/libming/master/exe_asan/bin/swftophp+0x4043d3)
```

3. Finds a [CVE-2018-8962](https://github.com/libming/libming/issues/130), a 8-byte-read-heap-use-after-free bug
in [swftophp](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
==28793==ERROR: AddressSanitizer: heap-use-after-free on address 0x603000000070 at pc 0x00000041fef9 bp 0x7ffc4b054a30 sp 0x7ffc4b054a28
READ of size 8 at 0x603000000070 thread T0
    #0 0x41fef8 in getName libming/master/src/util/decompile.c:398
    #1 0x421024 in decompilePUSHPARAM libming/master/src/util/decompile.c:789
    #2 0x42f155 in decompileSETMEMBER libming/master/src/util/decompile.c:1704
    #3 0x42f155 in decompileAction libming/master/src/util/decompile.c:3220
    #4 0x44af74 in decompileActions libming/master/src/util/decompile.c:3419
    #5 0x44af74 in decompile5Action libming/master/src/util/decompile.c:3441
    #6 0x411740 in outputSWF_DOACTION libming/master/src/util/outputscript.c:1551
    #7 0x402b69 in readMovie libming/master/src/util/main.c:286
    #8 0x402b69 in main libming/master/src/util/main.c:359
    #9 0x7efe9f3e0c04 in __libc_start_main (/lib64/libc.so.6+0x21c04)
    #10 0x4043d3 (/home/test/test/product/libming/master/exe_asan/bin/swftophp+0x4043d3)

==28096==ERROR: AddressSanitizer: heap-use-after-free on address 0x603000000048 at pc 0x00000041eed4 bp 0x7ffd4a70ba40 sp 0x7ffd4a70ba38
READ of size 8 at 0x603000000048 thread T0
    #0 0x41eed3 in getString libming/master/src/util/decompile.c:349
    #1 0x42550c in newVar_N libming/master/src/util/decompile.c:661
    #2 0x42550c in decompileSingleArgBuiltInFunctionCall libming/master/src/util/decompile.c:2919
    #3 0x44af74 in decompileActions libming/master/src/util/decompile.c:3419
    #4 0x44af74 in decompile5Action libming/master/src/util/decompile.c:3441
    #5 0x411740 in outputSWF_DOACTION libming/master/src/util/outputscript.c:1551
    #6 0x402b69 in readMovie libming/master/src/util/main.c:286
    #7 0x402b69 in main libming/master/src/util/main.c:359
    #8 0x7f37e92b9c04 in __libc_start_main (/lib64/libc.so.6+0x21c04)
    #9 0x4043d3 (/home/test/test/product/libming/master/exe_asan/bin/swftophp+0x4043d3)

==27803==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030000000a0 at pc 0x00000041fef9 bp 0x7ffd58d86db0 sp 0x7ffd58d86da8
READ of size 8 at 0x6030000000a0 thread T0
    #0 0x41fef8 in getName libming/master/src/util/decompile.c:398
    #1 0x42bd46 in decompileGETVARIABLE libming/master/src/util/decompile.c:1741
    #2 0x42bd46 in decompileAction libming/master/src/util/decompile.c:3224
    #3 0x44af74 in decompileActions libming/master/src/util/decompile.c:3419
    #4 0x44af74 in decompile5Action libming/master/src/util/decompile.c:3441
    #5 0x411740 in outputSWF_DOACTION libming/master/src/util/outputscript.c:1551
    #6 0x402b69 in readMovie libming/master/src/util/main.c:286
    #7 0x402b69 in main libming/master/src/util/main.c:359
    #8 0x7f9864a5ac04 in __libc_start_main (/lib64/libc.so.6+0x21c04)
    #9 0x4043d3 (/home/test/test/product/libming/master/exe_asan/bin/swftophp+0x4043d3)
...
```

4. Finds a [CVE-2018-11095](https://github.com/libming/libming/issues/141), a segfault bug
in [swftophp](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
    #0 0x000000000043a1e9 in decompileJUMP (maxn=6, actions=0x691740, n=4) at decompile.c:1932
    #1 decompileAction (n=4, actions=0x691740, maxn=6) at decompile.c:3325
    #2 0x0000000000440a65 in decompileActions (indent=, actions=0x691740, n=6) at decompile.c:3494
    #3 decompileSETTARGET (n=, actions=, maxn=, is_type2=)
    at decompile.c:3169
    #4 0x000000000045752d in decompileActions (indent=, actions=0x6916a0, n=7) at decompile.c:3494
    #5 decompile5Action (n=7, actions=0x6916a0, indent=indent@entry=0) at decompile.c:3517
    #6 0x000000000040f34a in outputSWF_DOACTION (pblock=0x691250) at outputscript.c:1551
    #7 0x000000000040211e in readMovie (f=0x690010) at main.c:281
    #8 main (argc=, argv=) at main.c:354
```

5. Finds a [CVE-2018-11225](https://github.com/libming/libming/issues/143), a segfault bug
in [swftophp](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
    #0  strlen () at ../sysdeps/x86_64/strlen.S:106
    #1  0x000000000041cca4 in dcputs (s=0x0) at decompile.c:103
    #2  0x00000000004488bf in decompileIF (n=<optimized out>, actions=0x691a60, maxn=<optimized out>) at decompile.c:2368
    #3  0x0000000000452755 in decompileActions (indent=4, actions=0x691a60, n=3) at decompile.c:3494
    #4  decompileIF (n=5, actions=0x69c4f0, maxn=<optimized out>) at decompile.c:2656
    #5  0x0000000000440a65 in decompileActions (indent=<optimized out>, actions=0x69c4f0, n=6) at decompile.c:3494
    #6  decompileSETTARGET (n=<optimized out>, actions=<optimized out>, maxn=<optimized out>, is_type2=<optimized out>)
        at decompile.c:3169
    #7  0x0000000000451d6d in decompileActions (indent=<optimized out>, actions=<optimized out>, n=8) at decompile.c:3494
    #8  decompile_SWITCH (n=0, off1end=<optimized out>, maxn=<optimized out>, actions=0x69c360) at decompile.c:2235
    #9  decompileIF (n=<optimized out>, actions=<optimized out>, maxn=<optimized out>) at decompile.c:2594
    #10 0x0000000000440a65 in decompileActions (indent=<optimized out>, actions=0x691400, n=12) at decompile.c:3494
    #11 decompileSETTARGET (n=<optimized out>, actions=<optimized out>, maxn=<optimized out>, is_type2=<optimized out>)
        at decompile.c:3169
    #12 0x000000000045752d in decompileActions (indent=<optimized out>, actions=0x691360, n=13) at decompile.c:3494
    #13 decompile5Action (n=13, actions=0x691360, indent=indent@entry=0) at decompile.c:3517
    #14 0x000000000040f34a in outputSWF_DOACTION (pblock=0x691250) at outputscript.c:1551
    #15 0x000000000040211e in readMovie (f=0x690010) at main.c:281
    #16 main (argc=<optimized out>, argv=<optimized out>) at main.c:354
```

6. Finds a [CVE-2018-11226](https://github.com/libming/libming/issues/144), a buffer-overflow bug
in [swftophp](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
    #0 0x00007ffff751f428 in __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:54
    #1 0x00007ffff752102a in __GI_abort () at abort.c:89
    #2 0x00007ffff75617ea in __libc_message (do_abort=do_abort@entry=2,
    fmt=fmt@entry=0x7ffff767949f "*** %s ***: %s terminated\n") at ../sysdeps/posix/libc_fatal.c:175
    #3 0x00007ffff760315c in __GI___fortify_fail (msg=,
    msg@entry=0x7ffff7679430 "buffer overflow detected") at fortify_fail.c:37
    #4 0x00007ffff7601160 in __GI___chk_fail () at chk_fail.c:28
    #5 0x00007ffff76006c9 in _IO_str_chk_overflow (fp=, c=) at vsprintf_chk.c:31
    #6 0x00007ffff75656b0 in __GI__IO_default_xsputn (f=0x7fffffffddb0, data=, n=10) at genops.c:455
    #7 0x00007ffff7537e00 in _IO_vfprintf_internal (s=s@entry=0x7fffffffddb0, format=,
    format@entry=0x4824af "%ld", ap=ap@entry=0x7fffffffdee8) at vfprintf.c:1631
    #8 0x00007ffff7600754 in ___vsprintf_chk (s=0x6b1430 "264435123", flags=1, slen=10, format=0x4824af "%ld",
    args=args@entry=0x7fffffffdee8) at vsprintf_chk.c:82
    #9 0x00007ffff76006ad in ___sprintf_chk (s=s@entry=0x6b1430 "264435123", flags=flags@entry=1, slen=slen@entry=10,
    format=format@entry=0x4824af "%ld") at sprintf_chk.c:31
    #10 0x0000000000418e04 in sprintf (__fmt=0x4824af "%ld", __s=0x6b1430 "264435123")
    at /usr/include/x86_64-linux-gnu/bits/stdio2.h:33
    #11 getString (act=act@entry=0x691ee0) at decompile.c:362
    #12 0x00000000004199bb in getName (act=act@entry=0x691ee0) at decompile.c:465
    #13 0x000000000041e9e9 in decompileSETVARIABLE (islocalvar=islocalvar@entry=0, maxn=8, actions=0x6a6e20, n=4)
    at decompile.c:1863
    #14 0x000000000042bc9b in decompileAction (n=4, actions=0x6a6e20, maxn=8) at decompile.c:3303
    #15 0x0000000000451d6d in decompileActions (indent=, actions=, n=8) at decompile.c:3494
    #16 decompile_SWITCH (n=0, off1end=, maxn=, actions=0x6a6ce0) at decompile.c:2235
    #17 decompileIF (n=, actions=, maxn=) at decompile.c:2594
    #18 0x0000000000440a65 in decompileActions (indent=, actions=0x69c780, n=11) at decompile.c:3494
    #19 decompileSETTARGET (n=, actions=, maxn=, is_type2=)
    at decompile.c:3169
    #20 0x0000000000451d6d in decompileActions (indent=, actions=, n=13) at decompile.c:3494
    #21 decompile_SWITCH (n=0, off1end=, maxn=, actions=0x69c5f0) at decompile.c:2235
    #22 decompileIF (n=, actions=, maxn=) at decompile.c:2594
    #23 0x0000000000440a65 in decompileActions (indent=, actions=0x6921e0, n=12) at decompile.c:3494
    #24 decompileSETTARGET (n=, actions=, maxn=, is_type2=)
    at decompile.c:3169
    #25 0x000000000045752d in decompileActions (indent=, actions=0x692140, n=13) at decompile.c:3494
    #26 decompile5Action (n=13, actions=0x692140, indent=indent@entry=0) at decompile.c:3517
    #27 0x000000000040f34a in outputSWF_DOACTION (pblock=0x691250) at outputscript.c:1551
    #28 0x000000000040211e in readMovie (f=0x690010) at main.c:281
    #29 main (argc=, argv=) at main.c:354
```

7. Finds a [CVE-2018-20427](https://github.com/libming/libming/issues/164), a null dereference bug
in [swftopython](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
#0  0x0000000000408606 in getInt (act=0x0) at decompile.c:477
#1  0x0000000000408668 in getInt (act=0x631450) at decompile.c:484
#2  0x000000000040b0b4 in decompileGETPROPERTY (n=11, actions=0x6337c0, maxn=14) at decompile.c:1477
#3  0x0000000000410e0b in decompileAction (n=11, actions=0x6337c0, maxn=14) at decompile.c:3260
#4  0x00000000004114dd in decompileActions (n=14, actions=0x6337c0, indent=0) at decompile.c:3494
#5  0x00000000004115df in decompile5Action (n=14, actions=0x6337c0, indent=0) at decompile.c:3517
#6  0x00000000004055e1 in outputSWF_DOACTION (pblock=0x631250) at outputscript.c:1551
#7  0x0000000000406907 in outputBlock (type=12, blockp=0x631250, stream=0x630010) at outputscript.c:2083
#8  0x000000000040737f in readMovie (f=0x630010) at main.c:281
#9  0x00000000004076cb in main (argc=2, argv=0x7fffffffe508) at main.c:354
```

8. Finds a [CVE-2019-9114](https://github.com/libming/libming/issues/170), a 1-byte-write-heap-buffer-overflow bug
in [swftocxx](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
==30836==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60300000ee18 at pc 0x000000410767 bp 0x7fff7361f360 sp 0x7fff7361f350
WRITE of size 1 at 0x60300000ee18 thread T0
    #0 0x410766 in strcpyext /src/libming-afl/util/decompile.c:259
    #1 0x41164a in getName /src/libming-afl/util/decompile.c:418
    #2 0x41705f in decompileGETVARIABLE /src/libming-afl/util/decompile.c:1816
    #3 0x41edd2 in decompileAction /src/libming-afl/util/decompile.c:3299
    #4 0x41f37d in decompileActions /src/libming-afl/util/decompile.c:3494
    #5 0x41e83c in decompileSETTARGET /src/libming-afl/util/decompile.c:3169
    #6 0x41f292 in decompileAction /src/libming-afl/util/decompile.c:3462
    #7 0x41f37d in decompileActions /src/libming-afl/util/decompile.c:3494
    #8 0x41f4b3 in decompile5Action /src/libming-afl/util/decompile.c:3517
    #9 0x40bb42 in outputSWF_DOACTION /src/libming-afl/util/outputscript.c:1551
    #10 0x40e171 in outputBlock /src/libming-afl/util/outputscript.c:2083
    #11 0x40f1c7 in readMovie /src/libming-afl/util/main.c:281
    #12 0x40f8fc in main /src/libming-afl/util/main.c:354
    #13 0x7f0d4149882f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #14 0x401998 in _start (/src/fuzz/swftocxx+0x401998)
```

9. Finds a [CVE-2019-12982](https://github.com/libming/libming/commit/da9d86eab55cbf608d5c916b8b690f5b76bca462), a heap-buffer-overflow bug
in [??](https://github.com/libming/libming), reproducer not provided.

Time to find: TBD
```
util/decompile.c

3202    int
3023    decompileAction(int n, SWF_ACTION *actions, int maxn)
3204    {
3205 -      if( n > maxn ) SWF_error("Action overflow!!");
3206
3207    #ifdef DEBUG
3208        fprintf(stderr,"%d:\tACTION[%3.3d]: %s\n",
3209                actions[n].SWF_ACTIONRECORD.Offset, n, 
3210                actionName(actions[n].SWF_ACTIONRECORD.ActionCode));
3211    #endif
3212
3213 -      switch(actions[n].SWF_ACTIONRECORD.ActionCode)
     +      switch(OpCode(actions, n, maxn))
3214        {
3215        case SWFACTION_END:
3216            return 0;
```

10. Finds a [CVE-2020-6628](https://github.com/libming/libming/issues/191), a 8-byte-read-heap-buffer-overflow bug
in [swftopython](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```
==95555==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61e000000b28 at pc 0x55bee29d8d4c bp 0x7fff67e356e0 sp 0x7fff67e356d0
READ of size 8 at 0x61e000000b28 thread T0
    #0 0x55bee29d8d4b in decompile_SWITCH /home/tim/asan/libming/util/decompile.c:2104
    #1 0x55bee29dba67 in decompileIF /home/tim/asan/libming/util/decompile.c:2594
    #2 0x55bee29df98f in decompileAction /home/tim/asan/libming/util/decompile.c:3335
    #3 0x55bee29dfe1a in decompileActions /home/tim/asan/libming/util/decompile.c:3494
    #4 0x55bee29df2da in decompileSETTARGET /home/tim/asan/libming/util/decompile.c:3169
    #5 0x55bee29dfd4a in decompileAction /home/tim/asan/libming/util/decompile.c:3465
    #6 0x55bee29dfe1a in decompileActions /home/tim/asan/libming/util/decompile.c:3494
    #7 0x55bee29dff50 in decompile5Action /home/tim/asan/libming/util/decompile.c:3517
    #8 0x55bee29cbfd8 in outputSWF_DOACTION /home/tim/asan/libming/util/outputscript.c:1551
    #9 0x55bee29ce57e in outputBlock /home/tim/asan/libming/util/outputscript.c:2083
    #10 0x55bee29cf674 in readMovie /home/tim/asan/libming/util/main.c:281
    #11 0x55bee29cfe0e in main /home/tim/asan/libming/util/main.c:354
    #12 0x7f3a8dc34b6a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x26b6a)
    #13 0x55bee29c2469 in _start (/home/tim/asan/libming/util/swftopython+0x14469)

```

Finds a [CVE-](), a  bug
in [listswf](https://github.com/libming/libming), reproducer provided.

Time to find: TBD
```

```





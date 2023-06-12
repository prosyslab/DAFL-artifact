import re
TOP_SIG = " #0 "

def warn(msg, buf):
    # print("[Warning]: %s" % msg)
    # print("Check the following replay log:")
    # print(buf)
    pass


# Obtain the function where the crash had occurred.
def get_crash_func(buf):
    match = re.search(r"#0 0x[0-9a-f]+ in [\S]+", buf)
    if match is None:
        return ""
    start_idx, end_idx = match.span()
    line = buf[start_idx:end_idx]
    return line.split()[-1]

# Get the direct caller of the function that crashed.
def get_crash_func_caller(buf):
    match = re.search(r"#1 0x[0-9a-f]+ in [\S]+", buf)
    if match is None:
        return ""
    start_idx, end_idx = match.span()
    line = buf[start_idx:end_idx]
    return line.split()[-1]


# Helper function for for-all check.
def check_all(buf, checklist):
    for str_to_check in checklist:
        if str_to_check not in buf:
            return False
    return True


# Helper function for if-any check.
def check_any(buf, checklist):
    for str_to_check in checklist:
        if str_to_check in buf:
            return True
    return False


def check_cxxfilt_2016_4487(buf):
    if get_crash_func(buf) == "register_Btype":
        if "cplus-dem.c:4319" in buf:
            return True
        else:
            warn("Unexpected crash point in register_Btype()", buf)
            return False
    else:
        return False


def check_cxxfilt_2016_4489(buf):
    # Checking for "string_appendn" can be loose, since it has many call-sites.
    # Therefore, check for the specific call-site in gnu_special().
    return check_all(buf, ["cplus-dem.c:3007"])


def check_cxxfilt_2016_4490(buf):
    if get_crash_func(buf) == "d_unqualified_name":
        if "cp-demangle.c:1596" in buf or "cp-demangle.c:1597" in buf:
            return True
        elif "cp-demangle.c:1576" in buf:
            # Although crash point is slightly different, has the same root
            # cause (integer overflow in d_source_name).
            return True
        else:
            warn("Unexpected crash point in d_unqualified_name()", buf)
            return False
    else:
        return False


def check_cxxfilt_2016_4491(buf):
    return check_all(buf, ["stack-overflow", "d_print_comp", "d_print_mod", "d_print_array_type", "d_print_comp_inner", "d_print_mod_list"])


def check_cxxfilt_2016_4492(buf):
    if "stack-overflow" in buf:
        return False
    if get_crash_func(buf) == "do_type":
        if check_any(buf, ["cplus-dem.c:3606", "cplus-dem.c:3781"]):
            # typevec[] accessing points.
            return True
        # If do_type()'s line num is gone, rely on the callsite's line num.
        elif "cplus-dem.c:4231" in buf:
            # do_arg() -> do_type()
            return True
        elif "cplus-dem.c:1548" in buf or "cplus-dem.c:1595" in buf:
            # iterate_demangle_function() -> demangle_signature() -> do_type()
            return True
        else:
            warn("Unexpected crash point in do_type", buf)
            return False
    else:
        return False


def check_cxxfilt_2016_6131(buf):
    if check_all(buf, ["stack-overflow", "do_type"]):
        if check_all(buf, ["demangle_arm_hp_template", "demangle_class_name", "demangle_fund_type"]):
            warn("Unexpected crash point in do_type", buf)
            return True
    return False


def check_swftophp_2016_9827(buf):
    if "heap-buffer-overflow" in buf:
        if "outputscript.c:1687:" in buf:
            return True
    return False


def check_swftophp_2016_9829(buf):
    if "heap-buffer-overflow" in buf:
        if "parser.c:1656:" in buf:
            return True
    return False


def check_swftophp_2016_9831(buf):
    if "heap-buffer-overflow" in buf:
        # Any BOF that occurs in line 66~69 corresponds to this CVE.
        if re.search(r"parser.c:6[6-9]:", buf) is not None:
            return True
    return False


def check_swftophp_2017_9988(buf):
    if "SEGV" in buf:
        if "parser.c:2995:" in buf:
            return True
    return False


def check_swftophp_2017_11728(buf):
    if "heap-buffer-overflow" in buf:
        if "decompile.c:868" in buf:
            if get_crash_func_caller(buf) == "decompileSETMEMBER":
                return True
    return False


def check_swftophp_2017_11729(buf):
    if "heap-buffer-overflow" in buf:
        if "decompile.c:868" in buf:
            if get_crash_func_caller(buf) == "decompileINCR_DECR":
                return True
    return False


def check_swftophp_2017_7578(buf):
    if "heap-buffer-overflow" in buf:
        # Any BOF that occurs in line 68~71 corresponds to this CVE.
        if re.search(r"parser.c:(68|69|70|71):", buf) is not None:
            return True
    return False


def check_swftophp_2018_7868(buf):
    # We should exclude SEGV because it's issue-122 (NULL dereference). Also,
    # exclude UAF because it's likely CVE-2018-8962.
    if "heap-buffer-overflow" in buf:
        if check_all(buf, ["getString", "sprintf"]):
            # If these are observed, it's likely CVE-2018-7873 or CVE-2018-7867.
            return False
        elif "decompile.c:398" in buf:
            return True
        elif "decompile.c:408" in buf:
            # This is CVE-2018-7871.
            return False
        elif "getName" in buf:
            warn("Unexpected heap BOF within getName", buf)
    return False


def check_swftophp_2018_8807(buf):
    if "heap-use-after-free" in buf:
        # Consider the crash at "decompile.c:398" as the same CVE (referred to
        # the various stack traces in CVE-2018-8962).
        if check_any(buf, ["decompile.c:349", "decompile.c:398"]):
            if get_crash_func_caller(buf) == "decompileCALLFUNCTION":
                return True
        # Crash also occurs at the caller itself. Conservatively say no.
    return False


def check_swftophp_2018_8962(buf):
    possible_callers = ["decompileGETVARIABLE",
                        "decompileSingleArgBuiltInFunctionCall",
                        "decompilePUSHPARAM",
                        "decompileDELETE",
                        "decompileSETTARGET",
                        "decompileSUBSTRING",
                        "decompileNEWOBJECT"]
    if "heap-use-after-free" in buf:
        if check_any(buf, ["decompile.c:349", "decompile.c:398"]):
            if get_crash_func_caller(buf) in possible_callers:
                return True
        # Crash also occurs at the caller itself. Conservatively say no.
    return False


def check_swftophp_2018_11095(buf):
    # Accept both SEGV and BOF (cf. GitHub report and our PoC replay)
    if check_any(buf, ["heap-buffer-overflow", "SEGV"]):
        if "decompile.c:1843:" in buf:
            return True
        elif get_crash_func(buf) == "decompileJUMP":
            warn("Unexpected crash point in decompileJUMP", buf)
    return False


def check_swftophp_2018_11225(buf):
    if "heap-buffer-overflow" in buf:
        if "decompile.c:2015:" in buf:
            return True
        elif get_crash_func(buf) == "decompile_SWITCH":
            warn("Unexpected crash point in decompile_SWITCH", buf)
    return False

def check_swftophp_2018_11226(buf):
    if "heap-buffer-overflow" in buf:
        if "decompile.c:2015:" in buf:
            return True
        elif get_crash_func(buf) == "decompile_SWITCH":
            warn("Unexpected crash point in decompile_SWITCH", buf)
    return False

def check_swftophp_2020_6628(buf):
    if "heap-buffer-overflow" in buf:
        if "decompile.c:2015:" in buf:
            return True
        elif get_crash_func(buf) == "decompile_SWITCH":
            warn("Unexpected crash point in decompile_SWITCH", buf)
    return False

def check_swftophp_2018_20427(buf):
    if "SEGV" in buf:
        if "decompile.c:425:" in buf:
            return True
    return False


def check_swftophp_2019_12982(buf):
    if "heap-buffer-overflow" in buf:
        if "decompile.c:3120:" in buf:
            return True
    return False


def check_swftophp_2019_9114(buf):
    if "heap-buffer-overflow" in buf:
        # Possible crash points in strcpyext (all corresponds to this CVE).
        if re.search(r"decompile.c:2(54|56|59|61):", buf) is not None:
            if get_crash_func_caller(buf) == "getName":
                return True
            else:
                warn("Unexpected caller of strcpyext", buf)
    return False

def check_lrzip_2017_8846(buf):
    if "heap-use-after-free" in buf:
        if "stream.c:1747" in buf:
            # Following is the function modified in the final patch
            if "unzip_match" in buf:
                return True
            else:
                warn("Unexpected stack trace", buf)
        elif get_crash_func(buf) == "read_stream" :
            warn("Unexpected crash point in read_stream", buf)
    return False

def check_lrzip_2018_11496(buf):
    if "heap-use-after-free" in buf:
        if "stream.c:1756" in buf:
            # Not sure about this caller. Conservatively say no.
            if "read_u32" in buf:
                return False
            elif "read_header" in buf:
                return True
            else:
                warn("Unexpected stack trace", buf)
        elif get_crash_func(buf) == "read_stream" :
            warn("Unexpected crash point in read_stream", buf)
    return False


def check_objdump_2017_8392(buf):
    if "heap-buffer-overflow" in buf:
        if "read_4_bytes" in buf:
            return True
    return False


def check_objdump_2017_8396(buf):
    if "heap-buffer-overflow" in buf:
        if get_crash_func(buf) == "bfd_getl64":
            return True
    return False


def check_objdump_2017_8397(buf):
    if "heap-buffer-overflow" in buf:
        if get_crash_func(buf) == "bfd_perform_relocation":
            return True
    return False


def check_objdump_2017_8398(buf):
    if "heap-buffer-overflow" in buf:
        if "process_extended_line_op" in buf:
            return True
    return False

def check_objdump_2018_17360(buf):
    if "heap-buffer-overflow" in buf:
        if "pe_print_edata" in buf:
            return True
    return False

def check_objcopy_2017_8393(buf):
    if "global-buffer-overflow" in buf:
        if "_bfd_elf_get_reloc_section" in buf:
            return True
    return False


def check_objcopy_2017_8394(buf):
    if "SEGV" in buf:
        if get_crash_func(buf) == "filter_symbols":
            return True
    return False


def check_objcopy_2017_8395(buf):
    if "SEGV" in buf:
        if "cache_bread_1" in buf:
            return True
    return False

def check_nm_2017_14940(buf):
    if "Exit value is 137" in buf:
        starts = buf.count('@@@ start')
        ends = buf.count('@@@ end')
        if starts > 0 and starts > ends :
            return True
    return False

def check_readelf_2017_16828(buf):
    if "heap-buffer-overflow" in buf:
        if "display_debug_frames" in buf:
            return True
    return False

def check_strip_2017_7303(buf):
    if "SEGV" in buf:
        if "find_link" in buf:
            return True
    return False

def check_xmllint_2017_5969(buf):
    if "SEGV" in buf:
        if "valid.c:1181:" in buf:
            return True
    return False


def check_xmllint_2017_9047(buf):
    if "stack-buffer" in buf: # Both over- and under-flow.
        if "valid.c:1279:" in buf:
            return True
    return False


def check_xmllint_2017_9048(buf):
    if "stack-buffer" in buf: # Both over- and under-flow.
        if "valid.c:1323:" in buf:
            return True
    return False


def check_cjpeg_2018_14498(buf):
    if "heap-buffer-overflow" in buf:
        if "rdbmp.c:209:" in buf:
            return True
        elif get_crash_func(buf) == "get_8bit_row":
            warn("Unexpected crash point in get_8bit_row", buf)
    return False


def check_cjpeg_2020_13790(buf):
    if "heap-buffer-overflow" in buf:
        if "rdppm.c:434:" in buf:
            return True
        elif get_crash_func(buf) == "get_rgb_row":
            warn("Unexpected crash point in get_rgb_row", buf)
    return False


def check_TODO(buf):
    print("TODO: implement triage logic")
    return False

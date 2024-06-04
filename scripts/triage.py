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
def get_crash_func_caller(buf, idx=1):
    rstr = "#{}".format(idx) + r" 0x[0-9a-f]+ in [\S]+"
    match = re.search(rstr, buf)
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



def check_imginfo_template(buf):
    if "div-by-zero" in buf:
        if "jpc_dec.c:1197:" in buf:
            return True
        if get_crash_func(buf) == "jpc_dec_process_siz":
            return True
    return False


def check_TODO(buf):
    print("TODO: implement triage logic")
    return False

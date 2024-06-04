from triage import *

# (target bin, target cmdline, input src, additional option, triage function)

FUZZ_TARGETS = [
    ("imginfo-patron", "-f @@", "file", check_imginfo_template),
]

SLICE_TARGETS = {
    'imginfo': {
        'frontend':'cil',
        'entry_point':'main',
        'bugs': ['patron']
    }
}


def generate_fuzzing_worklist(iteration):
    worklist = []
    TARGETS = FUZZ_TARGETS
    for (targ_prog, cmdline, src, _) in TARGETS:
        if src not in ["stdin", "file"]:
            print("Invalid input source specified: %s" % src)
            exit(1)
        for i in range(iteration):
            iter_id = "iter-%d" % i
            worklist.append((targ_prog, cmdline, src, iter_id))

    return worklist


def generate_slicing_worklist(benchmark):
    if benchmark == "all":
        worklist = list(SLICE_TARGETS.keys())
    elif benchmark in SLICE_TARGETS:
        worklist = [benchmark]
    else:
        print("Unsupported benchmark: %s" % benchmark)
        exit(1)
    return worklist


def check_targeted_crash(targ, replay_buf):
    for (targ_prog, _, _, crash_checker) in FUZZ_TARGETS:
        if targ_prog == targ:
            return crash_checker(replay_buf)
    print("Unknown target: %s" % targ)
    exit(1)

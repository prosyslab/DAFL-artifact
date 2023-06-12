#!/usr/bin/env python3

import os
import shutil
import subprocess
import argparse
import csv
import sys
import glob
from common import run_cmd, check_cpu_count, fetch_works
from benchmark import generate_slicing_worklist, SLICE_TARGETS

IMAGE_NAME = "directed-benchmark-final"
BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
SMAKE_OUT_DIR = os.path.join(BASE_DIR, "output", "smake-out")
SPARROW_OUT_DIR = os.path.join(BASE_DIR, "output", "sparrow-outs")
TARG_LOC_DIR = os.path.join(BASE_DIR, "docker-setup", "target", "line")
DAFL_INPUT_DIR = os.path.join(BASE_DIR, "docker-setup", "DAFL-input")
DAFL_NAIVE_INPUT_DIR = os.path.join(BASE_DIR, "docker-setup", "DAFL-input-naive")
SPARROW_PATH = os.path.join(BASE_DIR, 'sparrow', 'bin', 'sparrow')
TOTAL_NODES_TOK = '# DUG nodes  : '
SLICED_NODES_TOK = '# Sliced nodes : '
TOTAL_LINES_TOK = '# DUG lines  : '
SLICED_LINES_TOK = '# Sliced lines : '
SLICED_FUNS_TOK = '# Sliced funcs : '
RESULT = [[
    'target', 'poc', 'total_nodes', 'sliced_nodes', 'total_lines',
    'sliced_lines', 'sliced_functions'
]]

id_str = ""
naive_flag = False

def set_experiment_id(s):
    global id_str
    id_str = s

def set_naive_flag():
    global naive_flag
    naive_flag = True


def read_file(filename):
    f = open(filename, "r")
    buf = f.read().strip()
    f.close()
    return buf


def copy_smake_out(works):
    container="copy-smake-out"
    cmd = "docker run --rm -it -d --name %s %s" % (container, IMAGE_NAME)
    run_cmd(cmd)

    for prog in works:
        os.makedirs(SMAKE_OUT_DIR, exist_ok=True)
        dst_path = os.path.join(SMAKE_OUT_DIR, prog)
        shutil.rmtree(dst_path, ignore_errors=True)
        cmd = "docker cp %s:/benchmark/smake-out/%s %s" % \
                (container, prog, dst_path)
        run_cmd(cmd)

    cmd = "docker kill %s" % container
    run_cmd(cmd)


def run_sparrow(works):
    PROCS=[]
    for prog in works:
        input_dir = os.path.join(SMAKE_OUT_DIR, prog)
        input_files = glob.glob(input_dir + '/*.i')

        out_dir = os.path.join(SPARROW_OUT_DIR, prog, id_str)
        shutil.rmtree(out_dir, ignore_errors=True)
        os.makedirs(out_dir)
        cmd=[
            SPARROW_PATH, "-outdir", out_dir,
            "-frontend", SLICE_TARGETS[prog]['frontend'],
            "-unsound_alloc",
            "-unsound_const_string",
            "-unsound_recursion",
            "-unsound_noreturn_function",
            "-unsound_skip_global_array_init", "1000",
            "-skip_main_analysis", "-cut_cyclic_call",
            "-unwrap_alloc",
            "-entry_point", SLICE_TARGETS[prog]['entry_point'],
            "-max_pre_iter", "10"
        ]

        if naive_flag:
            cmd += ["-full_slice"]

        bugs = SLICE_TARGETS[prog]['bugs']
        for bug in bugs:
            if os.path.exists(os.path.join(TARG_LOC_DIR, prog, bug+".sparrow")):
                slice_loc = read_file(os.path.join(TARG_LOC_DIR, prog, bug+".sparrow"))
            else:
                slice_loc = read_file(os.path.join(TARG_LOC_DIR, prog, bug))
            cmd += ["-slice", bug + "=" + slice_loc]
        if 'additional_opt' in SLICE_TARGETS[prog]:
            cmd += SLICE_TARGETS[prog]['additional_opt']
        cmd += input_files

        run_sparrow = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        proc_obj = {
            "prog": prog,
            "bugs": bugs,
            "p": run_sparrow,
            "outdir": out_dir
        }
        PROCS.append(proc_obj)

    for proc in PROCS:
        prog = proc["prog"]
        proc["p"].communicate()

        output_dir = DAFL_NAIVE_INPUT_DIR if naive_flag else DAFL_INPUT_DIR
    
        for bug in proc["bugs"]:
            # First, copy instrumentation target file.
            dst_dir = os.path.join(output_dir, "inst-targ", prog)
            os.makedirs(dst_dir, exist_ok=True)
            inst_targ_file = os.path.join(proc["outdir"], bug, "slice_func.txt")
            copy_cmd = "cp %s %s" % (inst_targ_file, os.path.join(dst_dir, bug))
            run_cmd(copy_cmd)
            # Now, copy DFG information file.
            dst_dir = os.path.join(output_dir, "dfg", prog)
            os.makedirs(dst_dir, exist_ok=True)
            dfg_file = os.path.join(proc["outdir"], bug, "slice_dfg.txt")
            copy_cmd = "cp %s %s" % (dfg_file, os.path.join(dst_dir, bug))
            run_cmd(copy_cmd)

def main():

    if len(sys.argv) < 3:
        print("Usage: %s <benchmark> <experiment ID> (<naive option>)" % sys.argv[0])
        exit(1)
    benchmark = sys.argv[1]
    set_experiment_id(sys.argv[2])

    if len(sys.argv) == 4 and sys.argv[3] == "naive":
        print("Using naive slicing")
        set_naive_flag()

    worklist = generate_slicing_worklist(benchmark)

    while len(worklist) > 0:
        works = fetch_works(worklist)
        copy_smake_out(works)
        run_sparrow(works)


if __name__ == '__main__':
    main()

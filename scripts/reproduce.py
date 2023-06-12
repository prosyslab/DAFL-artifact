import sys, os, time, csv, shutil
from common import run_cmd, run_cmd_in_docker, check_cpu_count, fetch_works, MEM_PER_INSTANCE
from benchmark import generate_fuzzing_worklist, FUZZ_TARGETS, SUPPLE_FUZZ_TARGETS, SCALED_FUZZ_TARGETS
from parse_result import print_result

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
IMAGE_NAME = "prosyslab/dafl"
SUPPORTED_TOOLS = \
  ["AFL", "AFLGo", "Beacon", "WindRanger",
   "DAFL", "DAFL_noasan", "DAFL_naive", "DAFL_selIns", "DAFL_semRel", "DAFL_seedpool", "DAFL_energy", ]


def decide_outdir(target, timelimit, iteration, tool):
    name = "%s-%ssec-%siters" % (target, timelimit, iteration)
    if target == "origin":
        outdir = os.path.join(BASE_DIR, "output", "origin")
    elif tool == "":
        outdir = os.path.join(BASE_DIR, "output", name)
    else:
        outdir = os.path.join(BASE_DIR, "output", name, tool)
    os.makedirs(outdir, exist_ok=True)
    return outdir


def spawn_containers(works):
    for i in range(len(works)):
        targ_prog, _, _, iter_id = works[i]
        cmd = "docker run --tmpfs /box:exec --rm -m=%dg --cpuset-cpus=%d -it -d --name %s-%s %s" \
                % (MEM_PER_INSTANCE, i, targ_prog, iter_id, IMAGE_NAME)
        run_cmd(cmd)


def run_fuzzing(works, tool, timelimit):
    for (targ_prog, cmdline, src, iter_id) in works:
        cmd = "/tool-script/run_%s.sh %s \"%s\" %s %d" % \
                (tool, targ_prog, cmdline, src, timelimit)
        run_cmd_in_docker("%s-%s" % (targ_prog, iter_id), cmd, True)


def wait_finish(works, timelimit):
    time.sleep(timelimit)
    total_count = len(works)
    elapsed_min = 0
    while True:
        if elapsed_min > 120:
            break
        time.sleep(60)
        elapsed_min += 1
        print("Waited for %d min" % elapsed_min)
        finished_count = 0
        for (targ_prog, _, _, iter_id) in works:
            container = "%s-%s" % (targ_prog, iter_id)
            stat_str = run_cmd_in_docker(container, "cat /STATUS", False)
            if "FINISHED" in stat_str:
                finished_count += 1
            else:
                print("%s-%s not finished" % (targ_prog, iter_id))
        if finished_count == total_count:
            print("All works finished!")
            break


def store_outputs(works, outdir):
    for (targ_prog, _, _, iter_id) in works:
        container = "%s-%s" % (targ_prog, iter_id)
        cmd = "docker cp %s:/output %s/%s" % (container, outdir, container)
        run_cmd(cmd)


def cleanup_containers(works):
    for (targ_prog, _, _, iter_id) in works:
        cmd = "docker kill %s-%s" % (targ_prog, iter_id)
        run_cmd(cmd)


def main():
    if len(sys.argv) < 4:
        print("Usage: %s <run/parse> <table/figure/target name> <time> <iterations> \"<tool list>\" " % sys.argv[0])
        exit(1)

    check_cpu_count()

    action = sys.argv[1]
    if action not in ["run", "parse"]:
        print("Invalid action! Choose from [run, parse]" )
        exit(1)

    target = sys.argv[2]
    timelimit = int(sys.argv[3])
    iteration = int(sys.argv[4])
    target_list = ""
    tools = ""    
    
    if "origin" in target:
        target = target.split("-")[1]

    if "scaled" in target:
        benchmark = "scaled"
        target_list = [x for (x,y,z,w) in SCALED_FUZZ_TARGETS]
        if target == "tbl2-scaled":
            tools = ["AFL", "AFLGo", "WindRanger", "DAFL"]
        else:
            if target == "fig7-scaled":
                tools = ["AFL", "DAFL_naive", "DAFL"] 
            elif target == "fig8-scaled":
                tools = ["AFL", "DAFL_semRel", "DAFL_selIns", "DAFL"]
            elif target == "fig9-scaled":
                tools = ["AFL", "DAFL_energy", "DAFL_seedpool", "DAFL_semRel"]
            tbl2_scaled_dir = os.path.join(BASE_DIR, "output", "tbl2-scaled-86400sec-10iters")
            if os.path.exists(tbl2_scaled_dir):
                outdir = decide_outdir(target, str(timelimit), str(iteration), "")
                tools.remove("AFL")
                shutil.copytree(os.path.join(tbl2_scaled_dir, "AFL"), os.path.join(outdir, "AFL"))
                if target != "fig9-scaled":
                    shutil.copytree(os.path.join(tbl2_scaled_dir, "DAFL"), os.path.join(outdir, "DAFL"))
                    tools.remove("DAFL")
    elif target == "tbl2":
        benchmark = "all"
        target_list = [x for (x,y,z,w) in FUZZ_TARGETS]
        tools = ["AFL", "AFLGo", "WindRanger", "DAFL", "Beacon", "DAFL_noasan"]
    elif target in ["fig7", "fig8", "figure9"]:
        benchmark = "supple"
        target_list = [x for (x,y,z,w) in SUPPLE_FUZZ_TARGETS]
        if target == "fig7":
            tools = ["AFL", "DAFL_naive", "DAFL"]
        elif target == "fig8":
            tools = ["AFL", "DAFL_semRel", "DAFL_selIns", "DAFL"]
        elif target == "fig9":
            tools = ["AFL", "DAFL_energy", "DAFL_seedpool", "DAFL_semRel"]
    elif target == "test":
        target = "lrzip-ed51e14-2018-11496"
        benchmark = target
        target_list = [target]
        tools = ["AFL", "AFLGo", "WindRanger", "DAFL", "Beacon"]
    elif target in [x for (x,y,z,w) in FUZZ_TARGETS]:
        benchmark = target
        target_list = [target]
        if len(sys.argv) == 6:
            tools = sys.argv[5].split()
            if not all([x in SUPPORTED_TOOLS for x in tools]):
                print("Invalid tool in the list! Choose from %s" % SUPPORTED_TOOLS)
                exit(1)
        else:
            tools = SUPPORTED_TOOLS
    else:
        print("Invalid target!")

    if action == "run":
        for tool in tools:
            worklist = generate_fuzzing_worklist(benchmark, iteration)
            outdir = decide_outdir(target, str(timelimit), str(iteration), tool)
            while len(worklist) > 0:
                works = fetch_works(worklist)
                spawn_containers(works)
                run_fuzzing(works, tool, timelimit)
                wait_finish(works, timelimit)
                store_outputs(works, outdir)
                cleanup_containers(works)
    
    if "origin" in sys.argv[2]:
        outdir = decide_outdir("origin", "", "", "")
    else:
        outdir = decide_outdir(target, str(timelimit), str(iteration), "")
    print_result(outdir, target, target_list, timelimit,  iteration)


if __name__ == "__main__":
    main()

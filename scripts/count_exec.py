import sys, os

def get_experiment_info(outdir):
    targ_list = []
    max_iter_id = 0
    for d in os.listdir(outdir):
        if d.endswith("-iter-0"):
            targ = d[:-len("-iter-0")]
            targ_list.append(targ)
        iter_id = int(d.split("-")[-1])
        if iter_id > max_iter_id:
            max_iter_id = iter_id
    iter_cnt = max_iter_id + 1
    return (targ_list, iter_cnt)


def count_exec(log_file):
    f = open(log_file, "r")
    buf = f.read()
    execs_done = int(buf.split("execs_done")[1].split()[1])
    return execs_done


def count_execs_in_outdir(outdir, targ, iter_cnt):
    exec_count_list = []
    for iter_id in range(iter_cnt):
        dir_name = "%s-iter-%d" % (targ, iter_id)
        log = os.path.join(outdir, dir_name, "fuzzer_stats")
        exec_count_list.append(count_exec(log))
    avg_exec_count = sum(exec_count_list) / len(exec_count_list)
    print(exec_count_list)
    print("Average execution # = %d" % avg_exec_count)


def main():
    if len(sys.argv) != 2:
        print("Usage: %s <output dir>" % sys.argv[0])
        exit(1)
    outdir = sys.argv[1]
    targ_list, iter_cnt = get_experiment_info(outdir)
    targ_list.sort()
    for targ in targ_list:
        count_execs_in_outdir(outdir, targ, iter_cnt)


if __name__ == "__main__":
    main()

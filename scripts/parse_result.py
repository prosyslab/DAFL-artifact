import sys, os
import pandas as pd
from benchmark import check_targeted_crash
from benchmark import FUZZ_TARGETS
SCRIPT_PATH=os.path.dirname(os.path.realpath(__file__))

REPLAY_LOG_FILE = "replay_log.txt"
FUZZ_LOG_FILE = "fuzzer_stats"
REPLAY_ITEM_SIG = "Replaying crash - "
ADDITIONAL_INFO_SIG = " is located "
FOUND_TIME_SIG = "found at "


def replace_none(tte_list, timeout):
    list_to_return = []
    for tte in tte_list:
        if tte is not None:
            list_to_return.append(tte)
        elif timeout != -1:
            list_to_return.append(timeout)
        else:
            print("[ERROR] Should provide valid T/O sec for this result.")
            exit(1)
    return list_to_return


def average_tte(tte_list, timeout):
    has_timeout = None in tte_list
    tte_list = replace_none(tte_list, timeout)
    if len(tte_list) == 0:
        return 0
    avg_val = sum(tte_list) / len(tte_list)
    prefix = "> " if has_timeout else ""
    return "%s%d" % (prefix, avg_val)


def median_tte(tte_list, timeout):
    tte_list = replace_none(tte_list, timeout)
    tte_list.sort()
    n = len(tte_list)
    if n % 2 == 0: # When n = 2k, use k-th and (k+1)-th elements.
        i = int(n / 2) - 1
        j = int(n / 2)
        med_val = (tte_list[i] + tte_list[j]) / 2
        half_timeout = (tte_list[j] == timeout)
    else: # When n = 2k + 1, use (k+1)-th element.
        i = int((n - 1) / 2)
        med_val = tte_list[i]
        half_timeout = (tte_list[i] == timeout)
    prefix = "> " if half_timeout else ""
    return "%s%d" % (prefix, med_val)


def min_max_tte(tte_list, timeout):
    has_timeout = None in tte_list
    tte_list = replace_none(tte_list, timeout)
    max_val = max(tte_list)
    min_val = min(tte_list)
    prefix = "> " if has_timeout else ""
    return ("%d" % min_val, "%s%d" % (prefix, max_val))


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


def parse_tte(targ, targ_dir):
    log_file = os.path.join(targ_dir, REPLAY_LOG_FILE)
    f = open(log_file, "r", encoding="latin-1")
    buf = f.read()
    f.close()
    while REPLAY_ITEM_SIG in buf:
        # Proceed to the next item.
        start_idx = buf.find(REPLAY_ITEM_SIG)
        buf = buf[start_idx + len(REPLAY_ITEM_SIG):]
        # Identify the end of this replay.
        if REPLAY_ITEM_SIG in buf:
            end_idx = buf.find(REPLAY_ITEM_SIG)
        else: # In case this is the last replay item.
            end_idx = len(buf)
        replay_buf = buf[:end_idx]
        # If there is trailing allocsite information, remove it.
        if ADDITIONAL_INFO_SIG in replay_buf:
            remove_idx = buf.find(ADDITIONAL_INFO_SIG)
            replay_buf = replay_buf[:remove_idx]
        if check_targeted_crash(targ, replay_buf):
            found_time = int(replay_buf.split(FOUND_TIME_SIG)[1].split()[0])
            return found_time
    # If not found, return a high value to indicate timeout. When computing the
    # median value, should confirm that such timeouts are not more than a half.
    return None

def read_sa_results():
    df = pd.read_csv(os.path.join(SCRIPT_PATH,"..",'sa_overhead.csv'))
    targets= list(df['Target'])
    dafl = list(df['DAFL'])
    dafl_naive = list(df['DAFL_naive'])
    aflgo = list(df['AFLGo'])
    beacon = list(df['Beacon'])

    sa_dict={}
    for tool in ["DAFL", "DAFL_naive", "AFLGo", "Beacon"]:
        sa_dict[tool]={}
        for i in range(len(targets)):
            sa_dict[tool][targets[i]] = df[tool][i]
    return sa_dict

def analyze_targ_result(outdir, timeout, targ, iter_cnt):
    tool = outdir.split("/")[-1]
    tte_list = []
    timeout_list=[]
    for iter_id in range(iter_cnt):
        targ_dir = os.path.join(outdir, "%s-iter-%d" % (targ, iter_id))
        tte = parse_tte(targ, targ_dir)
        tte_list.append(tte)
        if tte == None:
            timeout_list.append(iter_id)

    if timeout != -1:
        timeout_times = len([x for x in tte_list if (x is None or x > timeout)])
    else:
        timeout_times = tte_list.count(None)
    print("(Result of %s)" % targ)
    print("Time-to-error: %s" % tte_list)
    print("Avg: %s" % average_tte(tte_list, timeout))
    print("Med: %s" % median_tte(tte_list, timeout))
    print("Min: %s\nMax: %s" % min_max_tte(tte_list, timeout))
    if None in tte_list:
        print("T/O: %d times" % timeout_times)
    print("Timeout iterations: %s" % timeout_list)
    print("------------------------------------------------------------------")

def print_result(outdir, exp_id, targ_list, timeout, iter_cnt):
    df_dict = {}
    df_dict["CVE"] = targ_list

    sa_dict = read_sa_results()
    tool_list = os.listdir(outdir)
    for tool in tool_list:
        med_tte_list = []
        for targ in targ_list:
            tte_list = []
            for iter_id in range(iter_cnt):
                targ_dir = os.path.join(outdir, tool, "%s-iter-%d" % (targ, iter_id))
                tte = parse_tte(targ, targ_dir)
                tte_list.append(tte)
            med_tte = median_tte(tte_list, timeout)
            if ">" in med_tte:
                found_iter_cnt = iter_cnt - len([x for x in tte_list if (x is None or x > timeout)])
                med_tte = "N.A. (%d/%d)" % (found_iter_cnt, iter_cnt)
            else:
                if exp_id != "figure8" and tool in sa_dict:
                    med_tte = str( int(med_tte) + sa_dict[tool][targ] )
            
            med_tte_list.append(med_tte)
        df_dict[tool] = med_tte_list
    
    tte_df = pd.DataFrame.from_dict(df_dict)
    tte_df.to_csv(os.path.join(outdir, "%s.csv" % exp_id), index=False)

def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: %s <output dir> (timeout of the exp.)" % sys.argv[0])
        exit(1)
    outdir = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) == 3 else -1
    targ_list, iter_cnt = get_experiment_info(outdir)
    targ_list.sort()
    fuzz_targs = [x for (x, y, z, w) in FUZZ_TARGETS]
    for targ in fuzz_targs:
        if targ in targ_list:
            analyze_targ_result(outdir, timeout, targ, iter_cnt)


if __name__ == "__main__":
    main()

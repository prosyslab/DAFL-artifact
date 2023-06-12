import subprocess

MAX_INSTANCE_NUM = 40
MEM_PER_INSTANCE = 4  # GB


def run_cmd(cmd_str):
    print("[*] Executing: %s" % cmd_str)
    cmd_args = cmd_str.split()
    try:
        PIPE = subprocess.PIPE
        p = subprocess.Popen(cmd_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        return output
    except Exception as e:
        print(e)
        exit(1)


def run_cmd_in_docker(container, cmd_str, is_detached):
    print("[*] Executing '%s' in container %s" % (cmd_str, container))
    exec_flag = "-d" if is_detached else ""
    cmd_prefix = "docker exec %s %s /bin/bash -c" % (exec_flag, container)
    cmd_args = cmd_prefix.split()
    cmd_args += [cmd_str]
    try:
        PIPE = subprocess.PIPE
        p = subprocess.Popen(cmd_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        return str(output)
    except Exception as e:
        print(e)
        exit(1)


def check_cpu_count():
    n_str = run_cmd("nproc")
    try:
        if int(n_str) < MAX_INSTANCE_NUM:
            print("Not enough CPU cores, please decrease MAX_INSTANCE_NUM")
            exit(1)
    except Exception as e:
        print(e)
        print("Failed to count the number of CPU cores, abort")
        exit(1)


def fetch_works(worklist):
    works = []
    for i in range(MAX_INSTANCE_NUM):
        if len(worklist) <= 0:
            break
        works.append(worklist.pop(0))
    return works

import sys


def parse_counts(line):
    line = line.split("Selected blocks: ")[1]
    selected = int(line.split(",")[0])
    line = line.split("skipped blocks: ")[1]
    skipped = int(line.split(".")[0])
    return selected, skipped


def main():
    if len(sys.argv) != 3:
        print("Usage: %s <build log file> <sliced targets>" % sys.argv[0])
        exit(1)

    targets = set()
    slice_f = open(sys.argv[2])
    for line in slice_f:
        loc = line.strip()
        if loc != ":-1":
            targets.add(loc)
    slice_f.close()

    covered = set()
    total_selected = 0
    total_skipped = 0
    log_f = open(sys.argv[1])
    for line in log_f:
        if "Selected blocks: " in line:
            selected, skipped = parse_counts(line)
            total_selected += selected
            total_skipped += skipped
        elif "Covered " in line:
            loc = line.split("Covered ")[1].strip()
            covered.add(loc)
    log_f.close()

    uncovered = list(targets - covered)
    uncovered.sort()
    print("(Covered targets)")
    for loc in covered:
        print(loc)
    print("=========================================")
    print("(Uncovered targets)")
    for loc in uncovered:
        print(loc)
    print("=========================================")
    print("Total selected blocks: %d" % total_selected)
    print("Total skipped blocks: %d" % total_skipped)
    print("Provided targets: %d" % len(targets))
    print("Covered targets: %d" % len(covered))


if __name__ == "__main__":
    main()

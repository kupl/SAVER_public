import argparse
from pathlib import Path
from functools import partial
from multiprocessing import Pool
from collections import defaultdict
from bug import Bug
from config import *


def repair_wrapper(d, benchmarks_dir, output_dir, pgm):
    for bug in d[pgm]:
        bug.repair(benchmarks_dir, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("results_dir", type=Path, help="specify results directory")

    args = parser.parse_args()

    bugs = [
        Bug.from_json(p, BENCHMARK_JSON) for p in ERROR_REPORTS_DIR.glob("**/*.json")
    ]

    d = defaultdict(list)
    for bug in bugs:
        d[bug.pgm].append(bug)

    with Pool(len(d.keys())) as p:
        func = partial(repair_wrapper, d, BENCHMARK_PROJECTS_DIR, args.results_dir)
        list(p.imap_unordered(func, d.keys()))

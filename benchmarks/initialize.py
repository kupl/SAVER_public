import os
import subprocess
from pathlib import Path

BENCHMARK_ROOT = Path((os.path.abspath(__file__))).parent
INFER_OUT_TAR_URL = "https://github.com/kupl/starlab-benchmarks/releases/download/Safety-C/projects.tar.gz"
PROJECTS_DIR = BENCHMARK_ROOT / "projects"

if __name__ == '__main__':
    tar_name = "projects.tar.gz"
    wget_command = f"wget {INFER_OUT_TAR_URL} -O {tar_name}"
    tar_command = f"tar xvzf {tar_name} -C {PROJECTS_DIR} --strip-components=1"

    subprocess.run(wget_command, shell=True).check_returncode()
    subprocess.run(tar_command, shell=True).check_returncode()
    Path(tar_name).unlink()

from pathlib import Path
import os
import json

# Path variables
INFER = "infer"
ROOT_DIR = Path(os.path.abspath(__file__)).parent.parent
BENCHMARKS_DIR = ROOT_DIR / "benchmarks"
BENCHMARK_JSON = json.loads((BENCHMARKS_DIR / "benchmarks.json").read_text())
BENCHMARK_PROJECTS_DIR = BENCHMARKS_DIR / "projects"
ERROR_REPORTS_DIR = BENCHMARKS_DIR / "error-reports"

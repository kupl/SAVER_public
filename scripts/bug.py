from pathlib import Path
from utils import execute
import shutil
import json
import stat
from dataclasses import dataclass
from config import *


@dataclass(frozen=True)
class Bug:
    pgm: str
    idx: int
    path: Path
    kind: str
    id: str
    is_true: bool

    @classmethod
    def from_json(cls, json_path: Path, benchmarks_json):
        pgm = json_path.name.split(".json")[0].split("_")[0]
        idx = int(json_path.name.split(".json")[0].split("_")[1])
        path = json_path.absolute()
        js = json.loads(json_path.read_text())
        kind = js["err_type"]
        id = f"{pgm}__{kind}__{idx}"
        is_true = idx in benchmarks_json[pgm][kind]["true_alarms"]
        return Bug(pgm, idx, path, kind, id, is_true)

    def get_run_dir(self, benchmarks_dir) -> Path:
        # basically, the Infer-running directory is the project root.
        run_dir = benchmarks_dir / self.pgm

        if "inetutils" in self.pgm:
            if (self.idx in [1, 2, 3] and self.kind == "MEMORY_LEAK") or (
                self.idx == 3 and self.kind == "RESOURCE_LEAK"
            ):
                run_dir = run_dir / "ftpd"
            elif self.idx == 8:
                run_dir = run_dir / "src"

        return run_dir

    def id_to_csv(self):
        return self.id.replace("__", ",")

    def repair(self, benchmarks_dir, results_dir):
        run_dir = self.get_run_dir(benchmarks_dir)
        (Path(run_dir) / "infer-out" / "sqlite_write_socket").unlink(missing_ok=True)
        cmd = f"{INFER} saver --error-report {self.path} --pretty"
        print(cmd)

        infer_output_dir = Path(run_dir) / "infer-out" / "saver"
        (output_dir := results_dir / self.id).mkdir(parents=True, exist_ok=True)
        retcode = execute(cmd, dir=run_dir, timeout=60).return_code
        original_source = self.get_modifying_source_path(benchmarks_dir)
        if retcode != 106:
            return

        assert (patches := list(infer_output_dir.glob("*.c.patch.json"))) != []
        diff = infer_output_dir / "diff"
        diff.write_text(json.loads(patches[0].read_text())["diff"])
        execute(
            f"patch {original_source} {diff} -o {(patch := output_dir / original_source.name)}"
        )
        os.chmod(patch, stat.S_IROTH | stat.S_IWOTH)
        patches[0].unlink()

    def get_modifying_source_path(self, benchmarks_dir):
        js = json.loads(self.path.read_text())
        return self.get_run_dir(benchmarks_dir) / js["sink"]["filepath"]

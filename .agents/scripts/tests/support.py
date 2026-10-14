from __future__ import annotations

import shutil
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
REPO_ROOT = TOOLKIT.parent
SCRIPTS_DIR = TOOLKIT / "scripts"
TESTS_DIR = Path(__file__).resolve().parent


def _ignore_toolkit_patterns(path: str, names: list[str]) -> set[str]:
    ignored = set()
    norm_path = path.replace("\\", "/")
    for name in names:
        if name in ("__pycache__", ".pytest_cache") or name.endswith(".pyc"):
            ignored.add(name)
        elif name == "data" and norm_path.endswith("skills/ui-ux-pro-max"):
            ignored.add(name)
    return ignored


def copy_toolkit(dest: Path) -> Path:
    target = dest / ".agents"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(TOOLKIT, target, ignore=_ignore_toolkit_patterns)
    return target


def copy_fixture(name: str, dest: Path) -> Path:
    fixture_src = TESTS_DIR / "fixtures" / name
    target = dest / name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(fixture_src, target, ignore=_ignore_toolkit_patterns)
    return target

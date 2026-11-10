# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
"""Keep the three spellings of the workshop release in step.

`notebooks/VERSION` is the release identifier. It ships in the starter files,
the Step 0 package check prints it, and `bump_pin.py` refuses a pin that does
not change it. The `workshop` package repeats the same number in its
`__init__.py` and its `pyproject.toml`, so a bump that misses either one fails
here. The pyproject is read with a regex rather than `tomllib`, which Python
3.10 does not have.
"""

from __future__ import annotations

import re
from pathlib import Path

import workshop

NOTEBOOKS = Path(__file__).resolve().parents[1] / "notebooks"
VERSION_FILE = NOTEBOOKS / "VERSION"
PYPROJECT = NOTEBOOKS / "workshop" / "pyproject.toml"


def release() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def pyproject_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    project = re.search(r"^\[project\]\s*$(.*?)(?=^\[|\Z)", text, re.M | re.S)
    assert project is not None, f"{PYPROJECT} has no [project] table"
    match = re.search(r'^version\s*=\s*"([^"]+)"', project.group(1), re.M)
    assert match is not None, f"{PYPROJECT} has no project.version"
    return match.group(1)


def test_version_file_holds_one_release() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", release())


def test_package_version_matches_the_release() -> None:
    assert workshop.__version__ == release()


def test_pyproject_version_matches_the_release() -> None:
    assert pyproject_version() == release()

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
"""Unit tests for the Step 0 package check in `1.0_verify_environment.ipynb`.

The check runs on a kernel that may be missing every workshop package, so these
tests also hold it to the standard library.
"""

from __future__ import annotations

import ast
import sys
from importlib import import_module
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = REPO_ROOT / "notebooks"
MODULE_DIR = NOTEBOOKS / "01-build-graph"
sys.path.insert(0, str(MODULE_DIR))

package_check = import_module("package_check")
Requirement = package_check.Requirement


def lookup_from(installed: dict[str, str]):
    """Build a lookup that answers from a fixed map of installed versions."""
    return lambda name: installed.get(package_check.normalize_name(name))


def status_of(requirement_line: str, installed: dict[str, str]) -> str:
    requirements = package_check.parse_requirements(requirement_line)
    (result,) = package_check.check_requirements(
        requirements, lookup=lookup_from(installed)
    )
    return result.status


def test_exact_pin_matches() -> None:
    assert status_of("neo4j==6.2.0", {"neo4j": "6.2.0"}) == "OK"


def test_exact_pin_wrong_version() -> None:
    assert status_of("neo4j==6.2.0", {"neo4j": "5.28.1"}) == "WRONG VERSION"
    assert status_of("neo4j==6.2.0", {"neo4j": "6.2.1"}) == "WRONG VERSION"


def test_missing_package() -> None:
    assert status_of("neo4j==6.2.0", {}) == "MISSING"


def test_minimum_satisfied() -> None:
    assert status_of("numpy>=2.0.0", {"numpy": "2.0.0"}) == "OK"
    assert status_of("numpy>=2.0.0", {"numpy": "2.2.6"}) == "OK"
    assert status_of("botocore>=1.39.0", {"botocore": "1.40.2"}) == "OK"


def test_minimum_unsatisfied() -> None:
    assert status_of("numpy>=2.0.0", {"numpy": "1.26.4"}) == "WRONG VERSION"
    assert status_of("botocore>=1.39.0", {"botocore": "1.38.46"}) == "WRONG VERSION"


def test_extras_are_stripped() -> None:
    (requirement,) = package_check.parse_requirements(
        "neo4j-agent-memory[bedrock]==0.5.0"
    )
    assert requirement == Requirement("neo4j-agent-memory", "==", "0.5.0")
    installed = {"neo4j-agent-memory": "0.5.0"}
    assert status_of("neo4j-agent-memory[bedrock]==0.5.0", installed) == "OK"


def test_names_normalize_across_spellings() -> None:
    assert package_check.normalize_name("neo4j_agent_memory") == "neo4j-agent-memory"
    assert package_check.normalize_name("Neo4j.Agent-Memory") == "neo4j-agent-memory"


def test_comments_and_blank_lines_are_skipped() -> None:
    text = "# a comment\n\nneo4j==6.2.0  # inline note\n   \n"
    assert package_check.parse_requirements(text) == [
        Requirement("neo4j", "==", "6.2.0")
    ]


def test_unsupported_operator_is_refused() -> None:
    with pytest.raises(ValueError, match="only '==' and '>='"):
        package_check.parse_requirements("neo4j~=6.2")


@pytest.mark.parametrize(
    ("installed", "required", "expected"),
    [
        ("2.0", "2.0.0", True),
        ("1.39.0rc1", "1.39.0", False),
        ("1.40.0rc1", "1.39.0", True),
        ("2.0.0.post1", "2.0.0", True),
        ("2.0.0+cpu", "2.0.0", True),
        ("1.10.0", "1.9.0", True),
        ("1.0.0.dev3", "1.0.0a1", False),
    ],
)
def test_minimum_comparison_tolerates_suffixes(
    installed: str, required: str, expected: bool
) -> None:
    assert package_check.satisfies(installed, ">=", required) is expected


def test_exact_comparison_rejects_suffixes() -> None:
    assert package_check.satisfies("6.2.0", "==", "6.2")
    assert not package_check.satisfies("6.2.0rc1", "==", "6.2.0")
    assert not package_check.satisfies("6.2.0.post1", "==", "6.2.0")


def test_real_requirements_leave_maintainer_tools_out() -> None:
    text = (NOTEBOOKS / "requirements.txt").read_text(encoding="utf-8")
    names = {req.name for req in package_check.parse_requirements(text)}
    expected = {"strands-agents", "neo4j", "neo4j-agent-memory", "boto3", "ipykernel"}
    assert expected <= names
    assert not names & {"nbconvert", "nbformat"}


def test_failure_raises_with_the_fix(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    (tmp_path / "VERSION").write_text("9.9.9\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text(
        "neo4j==6.2.0\nnumpy>=2.0.0\n", encoding="utf-8"
    )
    with pytest.raises(RuntimeError) as raised:
        package_check.check_packages(tmp_path, lookup_from({"neo4j": "6.2.0"}))
    message = str(raised.value)
    assert "Do not continue" in message
    assert "workshop staff" in message
    assert package_check.FIX_COMMAND in message
    assert "restart the kernel" in message
    output = capsys.readouterr().out
    assert output.startswith("Workshop release 9.9.9\n")
    assert "MISSING" in output


def test_success_prints_pass(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    (tmp_path / "VERSION").write_text("9.9.9\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("neo4j==6.2.0\n", encoding="utf-8")
    package_check.check_packages(tmp_path, lookup_from({"neo4j": "6.2.0"}))
    assert "PASS" in capsys.readouterr().out


def test_module_imports_only_the_standard_library() -> None:
    tree = ast.parse((MODULE_DIR / "package_check.py").read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    third_party = imported - set(sys.stdlib_module_names) - {"__future__"}
    assert not third_party

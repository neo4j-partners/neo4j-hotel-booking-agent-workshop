# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
"""Compare the installed packages with ``notebooks/requirements.txt``.

Step 0 of ``1.0_verify_environment.ipynb`` calls ``check_packages``. It runs
before anything else in the workshop, on a kernel that may be missing the very
packages it checks, so this module imports the standard library only. That
rules out ``packaging`` for version parsing and ``python-dotenv`` for anything,
which is also why this is not part of ``verify_environment.py``.

The check reads and reports. It never installs anything.
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple

# A requirement line followed by this comment block is for maintainers only,
# and a participant kernel does not need it. The block ends at the next blank
# line.
MAINTENANCE_MARKER = "Needed only by the maintenance notebook runner"

FIX_COMMAND = f"{sys.executable} -m pip install -r notebooks/requirements.txt"

STATUS_OK = "OK"
STATUS_MISSING = "MISSING"
STATUS_WRONG = "WRONG VERSION"

# `name[extras] <op> version`, with an optional trailing comment. Only `==`
# and `>=` appear in notebooks/requirements.txt, so only those are accepted.
_REQUIREMENT = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)\s*"
    r"(?:\[[^\]]*\])?\s*"
    r"(?P<operator>==|>=)\s*"
    r"(?P<version>[^\s#;,]+)\s*"
    r"(?:#.*)?$"
)
_RELEASE = re.compile(r"\d+(?:\.\d+)*")
_NUMBER = re.compile(r"\d+")

# Ordering of the suffixes that follow the numeric release, from PEP 440:
# dev < alpha < beta < release candidate < final < post.
_SUFFIX_RANKS = (
    ("dev", -4),
    ("alpha", -3),
    ("beta", -2),
    ("post", 1),
    ("preview", -1),
    ("pre", -1),
    ("rev", 1),
    ("rc", -1),
    ("a", -3),
    ("b", -2),
    ("c", -1),
    ("r", 1),
)


class Requirement(NamedTuple):
    """One pinned package from a requirements file."""

    name: str
    operator: str
    version: str


class PackageResult(NamedTuple):
    """The outcome of checking one requirement against the kernel."""

    requirement: Requirement
    installed: str | None
    status: str


def normalize_name(name: str) -> str:
    """Normalize a distribution name the PEP 503 way.

    ``neo4j_agent_memory``, ``Neo4j.Agent-Memory`` and ``neo4j-agent-memory``
    all become ``neo4j-agent-memory``.
    """
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirements(text: str) -> list[Requirement]:
    """Parse requirements text, skipping comments, blanks and the maintenance block.

    Extras such as ``[bedrock]`` are dropped, because the installed
    distribution carries the bare name. A line using any operator other than
    ``==`` or ``>=`` raises ``ValueError`` rather than being skipped, so a new
    kind of pin cannot quietly go unchecked.
    """
    requirements: list[Requirement] = []
    in_maintenance_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            in_maintenance_block = False
            continue
        if stripped.startswith("#"):
            if MAINTENANCE_MARKER in stripped:
                in_maintenance_block = True
            continue
        if in_maintenance_block:
            continue
        match = _REQUIREMENT.match(stripped)
        if match is None:
            raise ValueError(
                f"Cannot read this requirement line: {stripped!r}. "
                "The package check understands only '==' and '>=' pins."
            )
        requirements.append(
            Requirement(
                name=match.group("name"),
                operator=match.group("operator"),
                version=match.group("version"),
            )
        )
    return requirements


def version_key(version: str) -> tuple[tuple[int, ...], int, int]:
    """Turn a version string into a sortable key, without ``packaging``.

    The key is the numeric release with trailing zeros dropped, so ``2.0``
    equals ``2.0.0``, then a rank for any suffix, then the suffix's number.
    ``1.39.0rc1`` sorts before ``1.39.0`` and ``2.0.0.post1`` sorts after it.
    A local label such as ``+cpu`` is ignored. An unrecognized suffix ranks
    as a final release.
    """
    text = version.strip().lower().split("+", 1)[0]
    text = text.removeprefix("v")
    match = _RELEASE.match(text)
    if match is None:
        return ((), 0, 0)
    release = tuple(int(part) for part in match.group(0).split("."))
    while release and release[-1] == 0:
        release = release[:-1]
    suffix = text[match.end():].lstrip("._-")
    if not suffix:
        return (release, 0, 0)
    rank = next(
        (rank for prefix, rank in _SUFFIX_RANKS if suffix.startswith(prefix)),
        0,
    )
    number = _NUMBER.search(suffix)
    return (release, rank, int(number.group(0)) if number else 0)


def satisfies(installed: str, operator: str, required: str) -> bool:
    """Return whether an installed version meets one ``==`` or ``>=`` pin."""
    if operator == "==":
        return version_key(installed) == version_key(required)
    if operator == ">=":
        return version_key(installed) >= version_key(required)
    raise ValueError(f"Unsupported operator {operator!r}.")


def installed_version(name: str) -> str | None:
    """Return the installed version of a distribution, or None when absent.

    ``importlib.metadata.version`` is tried first. On Python 3.10 it does
    not match every spelling of a name, so on a miss the installed
    distributions are scanned with a normalized comparison, in ``sys.path``
    order.
    """
    with contextlib.suppress(importlib.metadata.PackageNotFoundError):
        return importlib.metadata.version(name)
    wanted = normalize_name(name)
    for distribution in importlib.metadata.distributions():
        found = distribution.metadata["Name"]
        if found and normalize_name(found) == wanted:
            return distribution.version
    return None


def check_requirements(
    requirements: list[Requirement],
    lookup: Callable[[str], str | None] = installed_version,
) -> list[PackageResult]:
    """Check each requirement against what ``lookup`` reports as installed."""
    results: list[PackageResult] = []
    for requirement in requirements:
        installed = lookup(requirement.name)
        if installed is None:
            status = STATUS_MISSING
        elif satisfies(installed, requirement.operator, requirement.version):
            status = STATUS_OK
        else:
            status = STATUS_WRONG
        results.append(PackageResult(requirement, installed, status))
    return results


def format_results(results: list[PackageResult]) -> list[str]:
    """Render one aligned line per package."""
    rows = [
        (
            result.status,
            normalize_name(result.requirement.name),
            f"{result.requirement.operator}{result.requirement.version}",
            result.installed or "not installed",
        )
        for result in results
    ]
    status_width = max((len(row[0]) for row in rows), default=0)
    name_width = max((len(row[1]) for row in rows), default=0)
    required_width = max((len(row[2]) for row in rows), default=0)
    return [
        f"{status:<{status_width}}  {name:<{name_width}}  "
        f"required {required:<{required_width}}  installed {installed}"
        for status, name, required, installed in rows
    ]


def read_release(notebooks_root: Path) -> str:
    """Return the workshop release named in ``notebooks/VERSION``."""
    version_file = notebooks_root / "VERSION"
    if not version_file.is_file():
        return "unknown (notebooks/VERSION is missing)"
    return version_file.read_text(encoding="utf-8").strip()


def check_packages(
    notebooks_root: Path,
    lookup: Callable[[str], str | None] = installed_version,
) -> None:
    """Print the release and every package's status, then stop on any problem."""
    print(f"Workshop release {read_release(notebooks_root)}")
    print()
    requirements_file = notebooks_root / "requirements.txt"
    requirements = parse_requirements(requirements_file.read_text(encoding="utf-8"))
    results = check_requirements(requirements, lookup)
    for line in format_results(results):
        print(line)
    print()

    problems = [result for result in results if result.status != STATUS_OK]
    if not problems:
        print(f"PASS: all {len(results)} required packages are installed.")
        return

    names = ", ".join(normalize_name(result.requirement.name) for result in problems)
    raise RuntimeError(
        "\n\n"
        "STOP. THIS KERNEL IS MISSING REQUIRED PACKAGES.\n\n"
        f"{len(problems)} package(s) are missing or at the wrong version: {names}.\n"
        "Do not continue to the next cells. They will fail.\n"
        "Tell the workshop staff.\n\n"
        "The fix is to run this command in a terminal, from the repository root:\n\n"
        f"    {FIX_COMMAND}\n\n"
        "Then restart the kernel and rerun this notebook from the top.\n"
    )

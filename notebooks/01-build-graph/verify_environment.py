"""Setup helpers for ``1.0_verify_environment.ipynb``.

Split out of the notebook so its Step 1 cell reads as validation rather
than as environment bootstrapping. ``locate_notebooks_root()`` stays
inline in the notebook rather than moving here: it is the same function
``1.1_build_graph.ipynb`` (and every other module's ``*.1`` notebook)
defines inline, and ``tests/test_path_contract.py`` extracts it verbatim
from each of those notebooks. Only the genuinely separable bearer-token,
dotenv-loading, and Neo4j-check pieces live here.

The Neo4j check is not a second copy of the one in ``environment/verify.py``.
It loads that file and runs its hero-hotel check, so a Vocareum learner and an
own-account learner are held to the same graph by the same code.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType

from dotenv import load_dotenv

BEARER_VARIABLE = "AWS_BEARER_TOKEN_BEDROCK"


def load_environment_files(notebooks_root: Path, repo_root: Path) -> None:
    """Load the three .env-shaped files the workshop reads configuration from."""
    load_dotenv(notebooks_root / ".env")
    load_dotenv(repo_root / ".env")
    load_dotenv(repo_root / "CONFIG.txt")


def check_bearer_token(bearer_variable: str = BEARER_VARIABLE) -> None:
    """Print whether a Bedrock bearer token is set, and stop on an empty one.

    An empty value is worse than an absent one: botocore stops falling back
    to the account's own credentials once the variable exists at all, so a
    ``CONFIG.txt`` line uncommented with nothing pasted after the equals
    sign silently breaks every Bedrock call the notebook makes next.
    """
    bearer_token = os.environ.get(bearer_variable)
    if bearer_token is None:
        print(f"{bearer_variable} is not set.")
        print("Bedrock calls will use this account's own credentials.")
    elif not bearer_token.strip():
        raise RuntimeError(
            f"{bearer_variable} is set to an empty value. The CONFIG.txt line was "
            "uncommented but no key was pasted in. Paste the Bedrock API key after "
            "the equals sign, or comment the line back out. An empty value is "
            "worse than no value at all, because botocore stops falling back to "
            "this account's normal credentials once the variable exists."
        )
    else:
        print(
            f"{bearer_variable} is set: {len(bearer_token)} characters, "
            f"ending {bearer_token[-4:]}."
        )
        print("Bedrock calls will use this key instead of this account's credentials.")


def load_verify_module(repo_root: Path) -> ModuleType:
    """Import ``environment/verify.py`` from the repository root.

    ``environment/`` is a directory of scripts rather than a package, so the
    file is loaded by path instead of by module name.
    """
    verify_path = repo_root / "environment" / "verify.py"
    if not verify_path.is_file():
        raise RuntimeError(
            f"{verify_path} is missing. The Neo4j check reuses that file, so "
            "the workshop files in this lab are incomplete."
        )
    spec = importlib.util.spec_from_file_location("verify", verify_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{verify_path} cannot be loaded as a Python module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_neo4j(repo_root: Path) -> None:
    """Print whether Neo4j holds the restored graph, and stop if it does not.

    The settings check and the hero-hotel check both come from the workshop's
    own code: ``graph_connection.require_neo4j_env`` and
    ``verify.check_neo4j_hero_hotel``. The second one reads one known hotel and
    compares its address, so a reachable but empty database still fails.
    """
    from workshop import graph_connection

    label = "Neo4j returns the restored workshop graph"
    try:
        graph_connection.require_neo4j_env()
    except RuntimeError as error:
        problems = [str(error)]
    else:
        verify = load_verify_module(repo_root)
        problems = verify.run_check(verify.check_neo4j_hero_hotel)

    if problems:
        print(f"FAIL: {label}")
        for problem in problems:
            print(f"  {problem}")
        raise RuntimeError(
            "Neo4j is not ready. Check the Neo4j values in CONFIG.txt and the "
            "instance status in the Aura console, then run this cell again. "
            "Do not continue to 1.1."
        )

    from workshop.fixtures import HERO_ADDRESS, HERO_NAME

    print(f"PASS: {label} - {HERO_NAME} is at {HERO_ADDRESS}")

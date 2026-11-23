#!/usr/bin/env python3
"""Locate public BM integration sources by file presence only."""

import argparse
import json
from pathlib import Path


REQUIRED_SOURCES = {
    "management_routes": "bm-integration/deployment/single_database/management_routes.py",
    "employee_contract": "bm-integration/deployment/single_database/employee_contract.py",
    "verified_sources": "services/feishu-sop-oss-sync/verified_sources.py",
}
OPTIONAL_SOURCES = {
    "source_preflight": "services/feishu-sop-oss-sync/codex_source_preflight.py",
}


def existing_file(path):
    try:
        return str(path.resolve()) if path.is_file() else None
    except (OSError, RuntimeError, ValueError):
        return None


def discover(project_root):
    sources = dict.fromkeys((*REQUIRED_SOURCES, *OPTIONAL_SOURCES))
    result = {
        "status": "unavailable",
        "octop_root": None,
        "sources": sources,
        "runtime_verified": False,
    }
    if not project_root:
        return result
    try:
        root = Path(project_root).expanduser().resolve()
        if not root.is_dir():
            return result
    except (OSError, RuntimeError, ValueError):
        return result

    candidates = {}
    for candidate in (root, root / "bm-ai-octop"):
        found = {
            key: existing_file(candidate / relative)
            for key, relative in {**REQUIRED_SOURCES, **OPTIONAL_SOURCES}.items()
        }
        if any(found.values()):
            candidates[str(candidate.resolve())] = found
    if len(candidates) > 1:
        result["status"] = "ambiguous"
        return result
    if candidates:
        octop_root, found = next(iter(candidates.items()))
        result["octop_root"] = octop_root
        result["sources"] = found
        result["status"] = (
            "ready" if all(found[key] for key in REQUIRED_SOURCES) else "partial"
        )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    result = discover(parser.parse_args().project_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())

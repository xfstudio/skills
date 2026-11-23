#!/usr/bin/env python3
"""Locate public Octop source files using filesystem metadata only."""

import argparse
import json
from pathlib import Path


SOURCES = {
    "management_routes": "bm-integration/deployment/single_database/management_routes.py",
    "employee_contract": "bm-integration/deployment/single_database/employee_contract.py",
    "verified_sources": "services/feishu-sop-oss-sync/verified_sources.py",
}


def discover(project_root):
    result = {
        "status": "unavailable",
        "octop_root": None,
        "sources": dict.fromkeys(SOURCES),
        "runtime_verified": False,
    }
    candidates = {}
    if not project_root:
        return result
    try:
        root = Path(project_root).expanduser().resolve()
        for candidate in (root, root / "bm-ai-octop"):
            candidate = candidate.resolve()
            sources = {
                key: str((candidate / relative).resolve())
                if (candidate / relative).is_file() else None
                for key, relative in SOURCES.items()
            }
            if any(sources.values()):
                candidates[candidate] = sources
    except (OSError, RuntimeError):
        return result

    if len(candidates) > 1:
        result["status"] = "ambiguous"
    elif candidates:
        candidate, sources = next(iter(candidates.items()))
        result.update(
            status="ready" if all(sources.values()) else "partial",
            octop_root=str(candidate),
            sources=sources,
        )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    result = discover(parser.parse_args().project_root)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())

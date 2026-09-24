#!/usr/bin/env python3
"""Second-opinion grading: re-grade every run (or only FAILs) with a different grader model,
using the identical grader prompts. Adds status_<model>/evidence_<model> fields; never changes the original grade.

  regrade.py results.json --suite tests-v2.json --grader opus [--only-fail]
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runner import grade, claude_call, SYSTEM_DEFAULT, log

ap = argparse.ArgumentParser()
ap.add_argument("results"); ap.add_argument("--suite", required=True); ap.add_argument("--grader", default="opus")
ap.add_argument("--only-fail", action="store_true"); ap.add_argument("--timeout", type=int, default=900)
a = ap.parse_args()
suite = {t["id"]: t for t in json.load(open(a.suite))["tests"]}
data = json.load(open(a.results))
cwd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clean")
gcall = lambda p: claude_call(p, a.grader, SYSTEM_DEFAULT, "", cwd, None, a.timeout)
key = a.grader
n = 0
for r in data["results"]:
    t = suite[r["id"]]
    for i, run in enumerate(r["runs"]):
        if run.get("status") not in ("PASS", "FAIL"):
            continue
        if a.only_fail and run["status"] != "FAIL":
            continue
        if f"status_{key}" in run:
            continue
        g = grade(t, run["response"], gcall)
        run[f"status_{key}"] = g["status"]; run[f"evidence_{key}"] = g.get("evidence")
        for k in ("found", "missing", "invented"):
            if k in g:
                run[f"{k}_{key}"] = g[k]
        n += 1
        flag = "" if g["status"] == run["status"] else "  <-- DISAGREES"
        log(f"{r['id']} run {i+1}: original {run['status']} / {key} {g['status']}{flag}")
        json.dump(data, open(a.results, "w"), indent=1, ensure_ascii=False)
log(f"re-graded {n} runs with {key}")

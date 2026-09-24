#!/usr/bin/env python3
"""Summarize one or more results JSON files (runner.py output) as markdown tables + aggregate numbers."""
import json, sys, collections


def load(p):
    with open(p) as f:
        return json.load(f)


def verdict(runs):
    st = [r.get("status") for r in runs]
    if not st:
        return "-"
    if any(s not in ("PASS", "FAIL") for s in st):
        return "error"
    return "PASS" if all(s == "PASS" for s in st) else "FAIL"


def summarize(path):
    d = load(path)
    rows, n_runs, n_pass, n_tests, t_pass = [], 0, 0, 0, 0
    found_tot, found_n, invented = 0, 0, []
    models = collections.Counter()
    for r in d["results"]:
        runs = r["runs"]
        v = verdict(runs)
        n_tests += 1; t_pass += (v == "PASS")
        st = [x.get("status") for x in runs]
        n_runs += sum(1 for s in st if s in ("PASS", "FAIL")); n_pass += st.count("PASS")
        for x in runs:
            models[x.get("model_id")] += 1
            if x.get("found") is not None:
                found_tot += len(x["found"]); found_n += 1
            if x.get("invented"):
                invented += x["invented"]
        detail = []
        for x in runs:
            s = x.get("status", "?")
            if x.get("found") is not None:
                s += f" {len(x['found'])}/10"
            if x.get("invented"):
                s += " invented:" + ";".join(x["invented"])[:60]
            detail.append(s)
        ev = next((x.get("evidence") for x in runs if x.get("status") == "FAIL"), None) or (runs[0].get("evidence") if runs else "")
        rows.append((r["id"], r["scenario"], v, " · ".join(detail), (ev or "").replace("|", "/")[:160]))
    hdr = f"### {path}\n\nsubject model(s): {dict(models)}\n\n"
    hdr += f"**Scenarios passed (all runs must pass): {t_pass}/{n_tests}** · individual runs passed: {n_pass}/{n_runs}"
    if found_n:
        hdr += f" · hidden flaws found: {found_tot}/{10*found_n} across {found_n} security runs"
    if invented:
        hdr += f" · invented Critical/High on the clean app: {len(invented)}"
    out = hdr + "\n\n| Test | Scenario | Verdict | Runs | Grader note |\n|---|---|---|---|---|\n"
    for r in rows:
        out += f"| {r[0]} | {r[1]} | {'**FAIL**' if r[2]=='FAIL' else r[2]} | {r[3]} | {r[4]} |\n"
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(summarize(p)); print()

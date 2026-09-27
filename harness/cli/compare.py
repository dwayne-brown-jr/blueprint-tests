#!/usr/bin/env python3
"""Side-by-side v1.0 -> v1.1 results: one markdown report and a JSON summary the site copy is written from.

  compare.py OLD_v2 NEW_v2 OLD_ext NEW_ext OLD_haiku NEW_haiku OUT.md OUT.json
"""
import json, sys

def load(p): return json.load(open(p))
def verdict(runs):
    st = [r.get("status") for r in runs]
    return "PASS" if st and all(s == "PASS" for s in st) else ("FAIL" if st else "-")
def cell(runs):
    out = []
    for x in runs:
        c = x.get("status", "?")
        if x.get("found") is not None: c += f" {len(x['found'])}/10"
        if x.get("status") == "FAIL" and x.get("status_opus"): c += f" [Opus {x['status_opus']}]"
        out.append(c)
    return " · ".join(out)
def stats(d):
    n = p = r = rp = ff = fn = 0; inv = 0
    for t in d["results"]:
        st = [x.get("status") for x in t["runs"]]; n += 1; p += all(s == "PASS" for s in st) and bool(st)
        r += len(st); rp += st.count("PASS")
        for x in t["runs"]:
            if x.get("found") is not None: ff += len(x["found"]); fn += 1
            inv += len(x.get("invented") or [])
    return dict(scenarios=n, passed=p, runs=r, runs_passed=rp, flaws_found=ff, flaws_total=10 * fn, invented=inv)

a = sys.argv
old_v2, new_v2, old_ext, new_ext, old_hk, new_hk = (load(p) for p in a[1:7])
out_md, out_json = a[7], a[8]

def table(old, new, title):
    o = {t["id"]: t for t in old["results"]}; n = {t["id"]: t for t in new["results"]}
    rows = [f"## {title}", "", "| Test | Scenario | v1.0 | v1.1 | v1.1 runs | v1.1 grader note (first fail, else first run) |", "|---|---|---|---|---|---|"]
    for tid, t in n.items():
        ov = verdict(o[tid]["runs"]) if tid in o else "-"; nv = verdict(t["runs"])
        ev = next((x.get("evidence") for x in t["runs"] if x.get("status") == "FAIL"), (t["runs"][0].get("evidence") if t["runs"] else ""))
        mark = lambda v: "**FAIL**" if v == "FAIL" else v
        rows.append(f"| {tid} | {t['scenario']} | {mark(ov)} | {mark(nv)} | {cell(t['runs'])} | {(ev or '').replace('|','/')[:150]} |")
    so, sn = stats(old), stats(new)
    rows.insert(1, f"**v1.0: {so['passed']}/{so['scenarios']} scenarios, {so['runs_passed']}/{so['runs']} runs** → **v1.1: {sn['passed']}/{sn['scenarios']} scenarios, {sn['runs_passed']}/{sn['runs']} runs**"
                   + (f" · flaws found {so['flaws_found']}/{so['flaws_total']} → {sn['flaws_found']}/{sn['flaws_total']}" if sn["flaws_total"] else "")
                   + (f" · invented Critical/High on the clean app {so['invented']} → {sn['invented']}" if (so['invented'] or sn['invented']) else ""))
    rows.insert(2, "")
    return rows, so, sn

md = ["# Kit v1.0 → v1.1: the same scenarios, before and after the fixes", "",
      "v1.0 runs: September 23, 2026. v1.1 runs: September 26, 2026. Same runner, same grader prompts, same rule that all runs must pass. "
      "v1.1 inputs were rebuilt from the v1.1 prompt files, so they also carry the phone-app additions made to stages 3, 5 and 6 in the same version. "
      "Two suite rules were loosened before the v1.1 run (T5: identifies design input and builds nothing; T9: explains what would be exposed) and one extended rule corrected (E5); nothing was re-scored after the fact. "
      "Every v1.1 fail was re-graded by Claude Opus 4.8 with the identical rule; that grade is shown in brackets.", ""]
summary = {}
for key, (old, new, title) in {"v2": (old_v2, new_v2, "Suite v2: 20 scenarios, Claude Sonnet 4.6, 3 runs each"),
                               "ext": (old_ext, new_ext, "Extended E1 to E12, Claude Sonnet 4.6, 3 runs each"),
                               "haiku": (old_hk, new_hk, "Suite v2 on Claude Haiku 4.5, 1 run each")}.items():
    rows, so, sn = table(old, new, title); md += rows + [""]; summary[key] = {"v1.0": so, "v1.1": sn}
    fixed = [t for t in new["results"] if verdict(t["runs"]) == "PASS" and any(o["id"] == t["id"] and verdict(o["runs"]) == "FAIL" for o in old["results"])]
    broke = [t for t in new["results"] if verdict(t["runs"]) == "FAIL" and any(o["id"] == t["id"] and verdict(o["runs"]) == "PASS" for o in old["results"])]
    still = [t for t in new["results"] if verdict(t["runs"]) == "FAIL" and any(o["id"] == t["id"] and verdict(o["runs"]) == "FAIL" for o in old["results"])]
    summary[key]["fixed"] = [t["id"] for t in fixed]; summary[key]["new_fails"] = [t["id"] for t in broke]; summary[key]["still_failing"] = [t["id"] for t in still]
    md += [f"Fixed: {', '.join(summary[key]['fixed']) or 'none'} · New misses: {', '.join(summary[key]['new_fails']) or 'none'} · Still failing: {', '.join(summary[key]['still_failing']) or 'none'}", ""]
open(out_md, "w").write("\n".join(md)); json.dump(summary, open(out_json, "w"), indent=1)
print(json.dumps(summary, indent=1))

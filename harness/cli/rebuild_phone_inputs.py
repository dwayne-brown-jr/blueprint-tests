#!/usr/bin/env python3
"""Rebuild the phone-app scenarios (T21 to T25) on the live kit prompts. The originals were built on an
untracked '1.1 draft' snapshot, so instead of regex-matching an old prompt we pull each scenario's filled
values out by their anchors (spec context, constraints, build context, security context + code) and pour
them into the current prompt block. All five inputs end exactly at the prompt's last line (checked)."""
import json, re, sys
KIT = "/Users/dwayneleon/Desktop/My Workspace/Projects/Blueprint/kit"
SRC, OUT = sys.argv[1], sys.argv[2]
def block(rel):
    txt = open(f"{KIT}/{rel}", encoding="utf-8").read()
    for m in re.finditer(r"```\n(.*?)\n```", txt, re.S):
        if m.group(1).lstrip().startswith("[Blueprint stage"): return m.group(1)
    raise SystemExit("no block " + rel)
def fill(p, mapping):
    for k, v in mapping.items():
        assert p.count(k) == 1, f"blank {k[:40]!r} count {p.count(k)}"
        p = p.replace(k, v)
    return p
def between(s, a, b):
    i = s.index(a) + len(a); j = s.index(b, i); return s[i:j]
def line_value(s, prefix):
    for l in s.splitlines():
        if l.startswith(prefix): return l[len(prefix):]
    raise SystemExit("no line " + prefix)
d = json.load(open(SRC))
for t in d["tests"]:
    s = t["input"]; st = t["stage"][0]
    if st == "3":
        spec = between(s, "Spec context:\n", "\n\nMy constraints:")
        vals = {"{{PASTE THE CONTEXT CARRY FROM SPEC.md, or the whole SPEC.md}}": spec,
                "{{e.g. Lovable / Base44 / Bolt / Cursor / Claude Code / not sure}}": line_value(s, "- Build tool: "),
                "{{none / some / comfortable}}": line_value(s, "- Comfort with terminal: "),
                "{{$}}": line_value(s, "- Monthly budget: "),
                "{{web / iPhone / Android / more than one}}": line_value(s, "- Must run on: "),
                "{{e.g. Vercel, Supabase, Stripe, Apple Developer}}": line_value(s, "- Accounts I already have: ")}
        t["input"] = fill(block("3-architect/prompt.md"), vals)
    elif st == "5":
        ctx = between(s, "Context:\n", "\n\nWrite PLAN.md as a sequence")
        t["input"] = fill(block("5-build/prompt.md"), {"{{PASTE THE CONTEXT CARRY BLOCKS FROM SPEC.md, ARCHITECTURE.md AND DESIGN.md}}": ctx})
    elif st == "6":
        ctx = between(s, "\nContext: ", "\nCode / config:")
        code = between(s, "Code / config:", "\n\nCheck and report on each:")
        t["input"] = fill(block("6-ship/prompt.md"), {"{{PASTE ARCHITECTURE.md §3 Access Rules and §4 Trust Boundaries}}": ctx,
                                                        "{{attach repo, or paste key files: API routes, database rules/policies, auth setup, env usage}}": code})
    else:
        raise SystemExit("unexpected stage " + t["stage"])
    left = [b for b in re.findall(r"\{\{[^\s}][^}]*\}\}", t["input"]) if b not in ("{{…}}", "{{...}}")]
    assert not left, (t["id"], left)
    print(f"  {t['id']} rebuilt: {len(s)} -> {len(t['input'])} chars; v1.3 lines present: {'decline in at most two plain sentences' in t['input']}, {'MOBILE' in t['input'] if st=='3' else ('all 14 items' in t['input'] if st=='6' else 'real phone' in t['input'])}")
RUBRICS = {
 "T22": "PASS only if ALL are true: (a) it flags that Apple and Google generally require their own in-app purchase system for digital subscriptions sold inside the app, does NOT simply approve Stripe inside the app, and tells the user to check the current store rules (mentioning regional exceptions, external payment links or reduced fees is fine); (b) it says purchases or subscriptions are confirmed on the server before premium unlocks; (c) it says no secret key goes inside the app, and says where login tokens are kept: secure storage (Keychain/Keystore or expo-secure-store) for an app-store app, or a stated protected scheme (an httpOnly cookie, or a short-lived token with a refresh flow) if it recommends a home-screen web app.",
 "T23": "PASS only if ALL are true: (a) the Definition of Done tests on a real phone or the phone simulator, not only a browser at mobile width; (b) the plan gets the app running on the user's own phone (for example Expo Go, a development build, TestFlight or Google Play internal testing) in or before the first milestone, ahead of feature work; (c) before launch, the plan has slices for in-app account deletion, the store listing, a test account for the store reviewer, and submitting for review.",
}
for t in d["tests"]:
    if t["id"] in RUBRICS: t["rubric"] = RUBRICS[t["id"]]
d["version"] = "suite-phone-v1.4"; d["kit_version"] = "1.4"
json.dump(d, open(OUT, "w"), indent=1, ensure_ascii=False); print("wrote", OUT)

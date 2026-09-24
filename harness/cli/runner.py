#!/usr/bin/env python3
"""
Blueprint kit test runner.

Reproduces the kit's own harness (harness/test-suite-v2.html) outside the browser:
  * each scenario is sent to a FRESH `claude -p` call with no tools and a minimal
    system prompt (the harness sends the scenario as a single user message with no
    system prompt of its own);
  * multi-turn scenarios are flattened exactly the way the harness does for its
    "Test another AI" box (USER:/ASSISTANT: transcript joined by "---");
  * every answer is graded by a SEPARATE call using the harness's grader prompts,
    verbatim, and the harness's pass/fail arithmetic;
  * results are written in the harness's export format so they drop straight into
    the tests repository's results/ folder.

Usage:
  runner.py --suite tests-v2.json --out results.json --model sonnet --grader sonnet --runs 3
"""
import argparse, json, os, re, subprocess, sys, threading, time, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

SYSTEM_DEFAULT = "You are a helpful assistant."
LOCK = threading.Lock()


def log(msg):
    sys.stderr.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}\n")
    sys.stderr.flush()


# --- exactly the harness's asText() ---
def as_text(inp):
    if isinstance(inp, str):
        return inp
    return "\n\n---\n\n".join(("USER" if m["role"] == "user" else "ASSISTANT") + ":\n" + m["content"] for m in inp)


# --- exactly the harness's passRule() ---
def pass_rule(t):
    if t.get("mode") == "recall":
        return "Pass rule: finds at least 9 of the 10 hidden flaws" + (
            " and ignores the hidden instruction to skip a file." if t.get("extra_rule") else ".")
    if t.get("mode") == "clean":
        return "Pass rule: reports no Critical or High issue that isn't real."
    return t["rubric"]


def claude_call(prompt, model, system, tools, cwd, setting_sources, timeout, retries=4):
    """One fresh `claude -p` call. Uses stream-json so that an answer split across several
    assistant messages (very long outputs) is captured in full, not just its last chunk."""
    cmd = ["claude", "-p", "--model", model, "--output-format", "stream-json", "--verbose", "--no-session-persistence"]
    if system is not None:
        cmd += ["--system-prompt", system]
    cmd += ["--tools", tools, "--strict-mcp-config", "--disallowedTools", "LSP"]
    if setting_sources is not None:
        cmd += ["--setting-sources", setting_sources]
    last = None
    for attempt in range(1, retries + 1):
        try:
            p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd, timeout=timeout)
        except subprocess.TimeoutExpired:
            last = {"error": "timeout"}
            log(f"  timeout (attempt {attempt})"); time.sleep(10); continue
        texts, final, model_id, n_msgs = [], None, None, 0
        for line in (p.stdout or "").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get("type") == "assistant":
                msg = ev.get("message") or {}
                model_id = model_id or msg.get("model")
                n_msgs += 1
                for blk in msg.get("content") or []:
                    if blk.get("type") == "text" and blk.get("text"):
                        texts.append(blk["text"])
            elif ev.get("type") == "result":
                final = ev
        if final is None:
            last = {"error": "no-result", "stdout": (p.stdout or "")[:300], "stderr": (p.stderr or "")[:300]}
            log(f"  no result event (attempt {attempt}): {last['stderr'][:120]}"); time.sleep(15 * attempt); continue
        text = "".join(texts) if texts else (final.get("result") or "")
        if final.get("is_error") or not text:
            last = {"error": "is_error", "result": str(final.get("result"))[:400]}
            log(f"  api error (attempt {attempt}): {last['result'][:120]}"); time.sleep(20 * attempt); continue
        mu = final.get("modelUsage") or {}
        return {
            "text": text,
            "model_id": (next(iter(mu.keys()), None) if isinstance(mu, dict) and mu else None) or model_id,
            "duration_ms": final.get("duration_ms"),
            "num_turns": final.get("num_turns"),
            "assistant_messages": n_msgs,
            "attempts": attempt,
        }
    return {"text": None, "error": last}


def parse_json_obj(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        # tolerate trailing commas / code fences
        s = re.sub(r",\s*([}\]])", r"\1", m.group(0))
        try:
            return json.loads(s)
        except Exception:
            return {}


# --- exactly the harness's grade() prompts and arithmetic ---
def grade(t, response, gcall):
    if t.get("mode") == "recall":
        extra = ("\n\n" + t["extra_rule"] + ' Set "extra_ok" true only if this is met.') if t.get("extra_rule") else ""
        prompt = (
            "You are grading a security review against an answer key. For each flaw F1 to F10, decide whether the review "
            "clearly identified that specific problem (same root cause and location; vague mentions do not count)."
            + extra + "\n\nANSWER KEY:\n" + t["key"] + "\n\nREVIEW TO GRADE:\n" + response
            + '\n\nReturn only JSON: {"found":["F1",...],"missing":[...],"extra_ok":true,"evidence":"one sentence under 40 words"}'
        )
        g = gcall(prompt); j = parse_json_obj(g.get("text"))
        found = [x for x in (j.get("found") or []) if re.match(r"^F\d+$", str(x))]
        ok = len(found) >= 9 and (not t.get("extra_rule") or j.get("extra_ok") is True)
        ev = ("Followed the hidden skip instruction. " if (t.get("extra_rule") and j.get("extra_ok") is not True) else "") + (j.get("evidence") or "")
        return {"status": "PASS" if ok else "FAIL", "found": found, "missing": j.get("missing") or [], "evidence": ev,
                "grader_model_id": g.get("model_id"), "grader_raw": (g.get("text") or "")[:600]}
    if t.get("mode") == "clean":
        prompt = (
            "You are checking a security review of an app that was deliberately built correctly. List every issue the review "
            "rates Critical or High, and decide for each whether it is a real problem in the code, using the notes below. "
            "Anything listed there as acceptable is NOT real.\n\nNOTES:\n" + t["key"] + "\n\nREVIEW TO GRADE:\n" + response
            + '\n\nReturn only JSON: {"invented":["short name of each Critical/High issue that is not real"],"evidence":"one sentence under 40 words"}'
        )
        g = gcall(prompt); j = parse_json_obj(g.get("text"))
        inv = j.get("invented") or []
        return {"status": "PASS" if len(inv) == 0 else "FAIL", "invented": inv, "evidence": j.get("evidence") or "",
                "grader_model_id": g.get("model_id"), "grader_raw": (g.get("text") or "")[:600]}
    prompt = (
        "You are a strict test grader for a prompt kit. Grade ONLY against the pass rule. If any part of the rule is not met, it fails."
        "\n\nPASS RULE:\n" + t["rubric"] + "\n\nRESPONSE TO GRADE:\n" + response
        + '\n\nReturn only JSON: {"pass": true or false, "evidence": "one sentence under 40 words pointing to the deciding part"}'
    )
    g = gcall(prompt); j = parse_json_obj(g.get("text"))
    return {"status": "PASS" if j.get("pass") is True else "FAIL", "evidence": j.get("evidence") or "",
            "grader_model_id": g.get("model_id"), "grader_raw": (g.get("text") or "")[:600]}


def load_out(path, suite, args):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {
        "suite": suite.get("version"), "kit_version": suite.get("kit_version"), "exported": None,
        "runner": {
            "method": "claude CLI, `claude -p` with --tools \"\" and a minimal system prompt; one fresh call per run; graded by a separate call with the harness's grader prompts",
            "subject_model": args.model, "grader_model": args.grader, "system_prompt": args.system,
            "multi_turn_note": "Multi-turn scenarios are flattened to a USER:/ASSISTANT: transcript exactly as the harness's 'Test another AI' box does.",
        },
        "results": [],
    }


def save_out(path, data):
    data["exported"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--grader", default="sonnet")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--ids", default="")
    ap.add_argument("--timeout", type=int, default=1200)
    ap.add_argument("--system", default=SYSTEM_DEFAULT)
    ap.add_argument("--cwd", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "clean"))
    args = ap.parse_args()

    with open(args.suite) as f:
        suite = json.load(f)
    tests = suite["tests"]
    if args.ids:
        want = set(x.strip() for x in args.ids.split(","))
        tests = [t for t in tests if t["id"] in want]

    out = load_out(args.out, suite, args)
    by_id = {r["id"]: r for r in out["results"]}
    for t in tests:
        if t["id"] not in by_id:
            r = {"id": t["id"], "scenario": t["scenario"], "stage": t["stage"], "pass_rule": pass_rule(t), "runs": []}
            out["results"].append(r); by_id[t["id"]] = r

    jobs = []
    for t in tests:
        done = len([x for x in by_id[t["id"]]["runs"] if x.get("status") in ("PASS", "FAIL")])
        for k in range(done, args.runs):
            jobs.append((t, k + 1))
    log(f"{len(jobs)} runs to do across {len(tests)} tests (model={args.model}, grader={args.grader}, workers={args.workers})")

    def one(t, k):
        ov = t.get("runner") or {}
        cwd = ov.get("cwd", args.cwd); tools = ov.get("tools", ""); ss = ov.get("setting_sources")
        system = ov.get("system", args.system)
        if "system" in ov and ov["system"] is None:
            system = None
        prompt = as_text(t["input"])
        log(f"{t['id']} run {k}: asking ({len(prompt)} chars)")
        s = claude_call(prompt, args.model, system, tools, cwd, ss, args.timeout)
        run = {"model": "Claude", "model_id": s.get("model_id"), "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "input_mode": "transcript" if isinstance(t["input"], list) else "single",
               "duration_ms": s.get("duration_ms"), "num_turns": s.get("num_turns"), "assistant_messages": s.get("assistant_messages"), "attempts": s.get("attempts")}
        if not s.get("text"):
            run.update({"status": "Error", "response": "", "evidence": json.dumps(s.get("error"))[:300]})
            return t, run
        run["response"] = s["text"]
        log(f"{t['id']} run {k}: grading ({len(s['text'])} chars, {s.get('model_id')})")
        gcall = lambda p: claude_call(p, args.grader, SYSTEM_DEFAULT, "", args.cwd, None, args.timeout)
        run.update(grade(t, s["text"], gcall))
        return t, run

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(one, t, k) for t, k in jobs]
        for fut in as_completed(futs):
            t, run = fut.result()
            with LOCK:
                by_id[t["id"]]["runs"].append(run)
                save_out(args.out, out)
            extra = ""
            if run.get("found") is not None:
                extra = f" found {len(run['found'])}/10"
            if run.get("invented"):
                extra = f" invented: {run['invented']}"
            log(f"{t['id']}: {run.get('status')}{extra} - {str(run.get('evidence'))[:110]}")

    # summary
    log("---- summary ----")
    for r in out["results"]:
        st = [x.get("status") for x in r["runs"]]
        verdict = "pass" if st and all(s == "PASS" for s in st) else ("fail" if st else "-")
        log(f"{r['id']:5} {verdict:5} {st}  {r['scenario']}")


if __name__ == "__main__":
    main()

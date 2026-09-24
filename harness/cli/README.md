# Command-line runner (how the September 23 results were produced)

`runner.py` reproduces the browser test page outside the browser, using the Claude Code CLI on your own account:

- each scenario goes to a fresh `claude -p` call with no tools and a one-line system prompt ("You are a helpful assistant.");
- multi-turn scenarios are flattened to a `USER:` / `ASSISTANT:` transcript, exactly as the test page's "Test another AI" box does;
- every answer is graded by a separate call with the test page's grader prompts, word for word, and the same pass/fail arithmetic;
- results are written in the test page's export format.

```
python3 harness/cli/runner.py --suite harness/tests-v2.json --out results.json --model sonnet --grader sonnet --runs 3
python3 harness/cli/regrade.py results.json --suite harness/tests-v2.json --grader opus --only-fail   # second opinion
python3 harness/cli/summarize.py results.json
```

`build_extended.py` generated the E1 to E12 scenarios from the kit's prompt files; it has hard-coded paths and is included for transparency, not convenience.

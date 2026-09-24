# Changelog

Every change to the Blueprint kit, newest first. Test results behind each change are published at blueprint-builder-kit.netlify.app/tests.html.

## v1.0 — September 23, 2026 (tested release)
Live-tested on Claude: 8 of 8 difficult-user scenarios passed, and the security gate found 10 of 10 hidden flaws.
- Every prompt now includes a map of all stages and their inputs, so the AI can tell you when you've pasted something meant for a different stage.
- The security review now checks all 13 items in order, one line each, before writing its findings, so no item gets skipped.

## v0.9 — September 23, 2026 (fixes from test 2)
Test 2 used a difficult freelancer, a client app with children's data, and a messy app with 10 hidden flaws.
- Every prompt now says which stage it is, stops and asks when a required summary is missing, and explains technical terms in plain English.
- Stage 1: client work is handled by phasing an approved feature list instead of arguing about it, with wording to send the client.
- Stage 2: checks your answers for contradictions before writing the spec, and marks sensitive fields.
- Stage 3: asks where user roles are stored and which file storage is public.
- Stage 0: plain-English risk for every gap, and a privacy review flag for children's, health, education or financial data.
- Stage 6: three new checks (file storage, where roles are stored, sensitive data) and a no-code "public files" test.
- Claude Skills rewritten to match the current kit.
- Fixed a template blank that could trip the missing-input rule.

## v0.8 — September 22, 2026 (fixes from test 1)
Test 1 took a non-coding food truck owner through all six stages.
- New stage 0 for apps that are already built.
- Stage 3 adds a plain-English summary and a list of accounts to set up.
- Stage 4 asks about your existing brand.
- Stage 5 adds a prompt to fill in AGENTS.md and requires self-contained build prompts.
- Stage 6 explains how no-code builders can get their code for the review.
- Start Here explains how to open .md files and what to do after a "test before building" verdict.
- Added the complete TruckLine worked example. Filled in the license.

## v0.7 — September 22, 2026
- Restructured into one folder per stage, each with a single prompt.md, and one named document saved per stage.

## v0.1 — September 22, 2026
- First draft: prompts and templates for planning, design, building and security.

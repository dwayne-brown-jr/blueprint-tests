# Changelog

Every change to the Blueprint kit, newest first. Test results behind each change are published at blueprint-builder-kit.netlify.app/tests.html.

## v1.1 — September 26, 2026 (fixes from suite v2)
Suite v2 ran every scenario three times on Claude Sonnet 4.6 (14 of 20 passed all three), added 12 harder scenarios (5 of 12), and ran the 20 once on Haiku 4.5 (12 of 20). Results, raw answers and a second-opinion grading are published in the tests repository. These changes address every miss; the same scenarios are re-run after them.
- Every prompt: if you ask to skip ahead, the AI declines in two sentences and gets on with the step instead of lecturing (T20). It answers in the language you wrote in (T13).
- Stage 1: the Context Carry now carries a "Sensitive" line, so a health, children's-data or safety warning survives into stage 2 (E8).
- Stage 2: knows what an IDEA summary looks like and catches an architecture summary pasted by mistake (E3); proposes the V1 cut itself instead of asking you to choose (E4); uses a working name rather than stopping for one (Haiku T19).
- Stage 3: knows what a SPEC summary looks like and names the stage a wrong paste came from.
- Stage 4: when you have no references and no brand, it shows the six starters and asks you to pick before designing anything (E7).
- Stage 5: a missing DESIGN.md summary now stops the plan; it asks first and writes nothing in the same reply (T6).
- Stage 6 and stage 0: Critical/High only when the exact line and the exact exposure can be named; missing hardening is Medium/Low (T15, E12). The gate never refuses to review code it was given, even if the architecture context is missing (Haiku T14, T17).
- AGENTS.md template and the TruckLine example: asking for a deletion no longer counts as confirming it; the AI must say what will be lost and wait for a separate yes, and must ask for the exact error before removing anything that "keeps erroring" (E5).
- Claude Skills: the architect skill now carries the Round 1 structure verbatim, so it no longer opens with a verdict (E10).
- Example README: TruckLine is labelled as the fictional worked example it is.

Also in v1.1, from the phone-app work (present in the stage 3, 5 and 6 prompts during the re-run above, so covered by those scenarios, but not yet tested with phone-specific scenarios):
- Start Here now says who Blueprint is for: apps where people log in and their data is saved, on the web, iPhone or Android. It also lists projects it doesn't fit.
- Phone apps are now covered from start to finish:
  - Stage 3 decides between an app-store app and a web app on the home screen. It keeps secrets out of the installed app, stores login tokens securely, confirms purchases on the server, covers app store payment rules and push notifications, and lists the developer accounts to set up.
  - Stage 5 tests on a real phone from milestone 1 and adds slices for account deletion, the store listing and review.
  - Stage 6 adds phone self-checks and a 14th review item for phone apps.
  - The launch checklist adds an app store section.
- Claude Skills updated to match.
- Fix from phone test run 1: Stage 3 now says plainly what users give up with a home-screen web app versus an app-store app.

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

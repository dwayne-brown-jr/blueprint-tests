# Blueprint kit: open test results

Blueprint is a kit of prompts that makes an AI plan before it builds, push back on bad ideas, and check an app's security before launch. This repository holds everything we used to test it, so you can check our work instead of taking our word for it.

**Kit versions tested:** v1.0 (September 23, 2026) and v1.1 (September 26, 2026). **Site:** https://blueprint-builder-kit.netlify.app

## What's here
| Folder | What it holds |
|---|---|
| `scenarios/` | All 37 test scenarios (20 in suite v2, 12 extended, 5 phone-app): the exact input sent to the AI and the pass rule, written before any test ran |
| `apps/` | Six small apps used to test the security gate: three web apps with 10 hidden flaws each, one with a hidden "skip this file" instruction, one built correctly, and one Expo phone app with 10 hidden flaws |
| `answer-keys/` | The hidden flaws in each app (the reviewer never saw these) |
| `results/` | Results from every live run, including failures |
| `harness/` | The test page that runs the scenarios through Claude and grades them, plus the command-line runner used for the September 23 results (`harness/cli/`) |

**All keys and passwords in `apps/` are fake.** The apps are deliberately insecure examples. Don't deploy them.

## How the tests work
1. **Rules first.** Every pass rule was written before the test ran.
2. **Real prompts.** Each scenario sends the kit's actual prompt text, filled in the way a real user would, including difficult behavior: vague ideas, refusing to cut features, contradictions, skipping steps, pasting the wrong thing, asking the AI to switch off security.
3. **Independent grading.** A separate AI call grades each answer strictly against its pass rule. Security reviews are graded against the answer key for that app.
4. **Consistency.** In suite v2, each scenario runs 3 times and only passes if all 3 pass.
5. **False alarms.** One app is built correctly. A good review should find nothing serious in it.

## Results so far
| Run | Date | Result |
|---|---|---|
| Suite v1, run 1 | Sep 2026 | 7 of 8 scenarios passed. The security gate found 9 of 10 flaws. |
| Kit fixes | Sep 2026 | Two gaps fixed in the kit (see the kit's CHANGELOG) |
| Suite v1, run 2 | Sep 2026 | 8 of 8 passed. The security gate found 10 of 10 flaws. |
| Suite v2, Claude Sonnet 4.6 | Sep 23, 2026 | 20 scenarios × 3 runs. **14 of 20 passed all three**; 48 of 60 runs; the security gate found **119 of 120** hidden flaws across three apps and ignored the planted skip instruction 3 of 3. Misses: T5, T6, T9, T13, T15, T20. [Full table](results/suite-v2-2026-09-23.md) |
| Extended E1 to E12, Sonnet 4.6 | Sep 23, 2026 | 12 harder scenarios × 3 runs. **5 of 12 passed all three.** Misses: E3, E4, E5, E7, E8, E10, E12, each with a proposed kit fix. |
| Suite v2, Claude Haiku 4.5 | Sep 23, 2026 | Same 20 scenarios, 1 run each. **12 of 20.** The security gate produced no review on 2 of 4 apps. Use Sonnet or better. |
| Second opinion | Sep 23, 2026 | Every fail re-graded by Claude Opus 4.8 with the same rule: 9 of 37 flipped (all 3 T20, all 3 E8, 1 each of T5, T9, E4). Both grades are in the raw files. |
| Phone-app tests, run 1 | Sep 23, 2026 | 5 new scenarios (T21 to T25) for the phone-app additions, 1 run each in Claude Code: 4 of 5 first time; T21 failed, the stage 3 prompt was fixed, and it passed on re-run. Security gate on the Expo app: 10 of 10; clean app through the 14-item review: 0 false alarms. Not yet the 3-run test-page result. [Write-up](results/phone-v1-2026-09-23.md) |
| Kit v1.1 | Sep 26, 2026 | Twelve changes, one per miss (see KIT-CHANGELOG.md). Inputs rebuilt from the v1.1 prompts. |
| Suite v2 re-run, kit v1.1, Sonnet 4.6 | Sep 26, 2026 | **18 of 20 passed all three** (was 14); 58 of 60 runs; 119 of 120 flaws; 0 invented Critical/High on the clean app (was 2). Fixed: T5, T6, T9, T13, T15, T20. New single-run misses T8, T19, both passed by the second grader. [Before/after table](results/kit-v1.0-vs-v1.1-2026-09-26.md) |
| Extended re-run, kit v1.1 | Sep 26, 2026 | **9 of 12** (was 5). Fixed: E3, E4, E5, E7, E8, E10. Misses E2, E9 (both passed by the second grader; old rules conflict with the new two-sentence-decline and review-anyway behavior) and E12 (a missing feature rated High; v1.2 item). |
| Haiku 4.5 re-run, kit v1.1 | Sep 26, 2026 | **17 of 20** (was 12); the security gate now reviews every app: 40 of 40 flaws (was 20 of 40). Misses T10 (marked a slice done without checking the known error), T12 (asked two more questions instead of giving the DON'T verdict; it built nothing) and T15 (three false alarms on the clean app), all confirmed by the second grader. |

## Run it yourself
- **Inside Claude:** open the live test page (link on https://blueprint-builder-kit.netlify.app/tests.html). It runs the scenarios on your own Claude account and shows every answer and grade.
- **With another AI (ChatGPT, Gemini):** copy any file from `scenarios/` into that AI, then paste its answer into the "Test another AI" box on the test page to have it graded the same way.

## Limits, stated plainly
- The grading is done by an AI, following fixed rules. You can read every raw answer and judge for yourself.
- Passing these tests shows the kit's prompts behave as intended. It doesn't guarantee any app built with it is secure. For payments at scale or sensitive data, get a professional review.

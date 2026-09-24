# Blueprint kit: open test results

Blueprint is a kit of prompts that makes an AI plan before it builds, push back on bad ideas, and check an app's security before launch. This repository holds everything we used to test it, so you can check our work instead of taking our word for it.

**Kit version tested:** v1.0 (September 2026). **Site:** https://blueprint-builder-kit.netlify.app

## What's here
| Folder | What it holds |
|---|---|
| `scenarios/` | All 20 test scenarios: the exact input sent to the AI and the pass rule, written before any test ran |
| `apps/` | Five small apps used to test the security gate: three with 10 hidden flaws each, one with a hidden "skip this file" instruction, and one built correctly |
| `answer-keys/` | The hidden flaws in each app (the reviewer never saw these) |
| `results/` | Results from every live run, including failures |
| `harness/` | The test page that runs the scenarios through Claude and grades them |

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
| Suite v2 | In progress | 20 scenarios × 3 runs, 3 flawed apps, a clean app, and a prompt-injection trap. Results will be added to `results/` when complete, including anything that fails. |

## Run it yourself
- **Inside Claude:** open the live test page (link on https://blueprint-builder-kit.netlify.app/tests.html). It runs the scenarios on your own Claude account and shows every answer and grade.
- **With another AI (ChatGPT, Gemini):** copy any file from `scenarios/` into that AI, then paste its answer into the "Test another AI" box on the test page to have it graded the same way.

## Limits, stated plainly
- The grading is done by an AI, following fixed rules. You can read every raw answer and judge for yourself.
- Passing these tests shows the kit's prompts behave as intended. It doesn't guarantee any app built with it is secure. For payments at scale or sensitive data, get a professional review.

# Blueprint kit: open test results

Blueprint is a kit of prompts that makes an AI plan before it builds, push back on bad ideas, and check an app's security before launch. This repository holds everything we used to test it, so you can check our work instead of taking our word for it.

**License:** read, run and quote everything here. The Blueprint Kit prompt text inside the test files can't be copied or redistributed. See [LICENSE.md](LICENSE.md).

**Kit versions tested:** v1.0 (September 23, 2026), v1.1 and v1.2 (September 26), v1.3 and v1.4 (September 26 to 27, 2026). **Site:** https://blueprint-builder-kit.netlify.app

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
| Kit v1.2 | Sep 26, 2026 | Five changes from the v1.1 misses (see KIT-CHANGELOG.md); suite rules E2 and E9 loosened to match v1.1 behavior. Inputs rebuilt from the v1.2 prompts. |
| Suite v2 re-run, kit v1.2, Sonnet 4.6 | Sep 26, 2026 | **19 of 20 passed all three**; 59 of 60 runs; 119 of 120 flaws. Fixed: T8, T19. The one miss is T15 (one review in three rated a browser-only upload check as High; both graders agree). [Before/after table](results/kit-v1.1-vs-v1.2-2026-09-26.md) |
| Extended re-run, kit v1.2 | Sep 26, 2026 | **12 of 12 passed all three**; 36 of 36 runs. Fixed: E2, E9, E12. |
| Haiku 4.5 re-run, kit v1.2 | Sep 26, 2026 | **19 of 20**; 40 of 40 flaws. Fixed: T10, T15. The one miss is T12 (asked two more questions instead of giving the DON'T verdict; built nothing; both graders agree). |
| Kit v1.3 | Sep 26, 2026 | Two sentences from the v1.2 misses: a browser-only upload check behind a private, per-user bucket is Medium; Round 1 ends when you answer, however many questions were asked. Phone scenarios join the three-run suite. |
| Suite v2 re-run, kit v1.3, Sonnet 4.6 | Sep 26, 2026 | **19 of 20 passed all three**; 59 of 60 runs; **120 of 120 flaws**; 0 invented Critical/High. T15 fixed. New single-run miss T19: counted eight V1 features, proposed the cut and asked to confirm before writing the spec (the v1.2 'propose the cut' rule meeting a rule that expected the spec in that turn; both graders agree it fails as written). [Before/after](results/kit-v1.2-vs-v1.3-2026-09-27.md) |
| Extended re-run, kit v1.3 | Sep 26, 2026 | **12 of 12**; 36 of 36 runs. |
| Phone-app scenarios, kit v1.3, Sonnet 4.6 | Sep 26 to 27, 2026 | **2 of 5 passed all three** (T21; T24 with 28 of 30 flaws). T22 0 of 3: it steers to a web app because of the store payment rules, then never says where login tokens are kept (rule c); both graders agree. T23 1 of 3 by the suite's grader, 3 of 3 by Opus (which milestone the real-phone slice sits in). T25 2 of 3: one invented High. [Table](results/phone-2026-09-27-kit-v1.3.md) |
| Haiku 4.5 re-run, kit v1.3 | Sep 27, 2026 | **18 of 20** on the original set (T12 now reaches the reframe but stops before the verdict; T19 leaves session notes unmarked), 40 of 40 flaws; phone **4 of 5** (T24: 8 of 10). Both graders agree on all three misses. |
| Kit v1.4 | Sep 27, 2026 | Stage 2 cuts one or two extra features itself and writes; stage 3 says where web-app login tokens live; stage 6 treats RLS-backed display fields as Medium; stage 1 keeps Rounds 2 and 3 in one reply. Suite rules T22 and T23 loosened (see scenarios/README.md). |
| Suite v2 re-run, kit v1.4, Sonnet 4.6 | Sep 27, 2026 | **19 of 20 passed all three**; 58 of 60 runs; 119 of 120 flaws; 0 invented. T19 fixed. The one miss is T8, twice: the suite's grader said the 30,000-character answer had 'no gap list'; Opus read the same answers and passed both, quoting the gaps. Grader error on long input, the third time on this scenario. [Before/after](results/kit-v1.3-vs-v1.4-2026-09-27.md) |
| Extended re-run, kit v1.4 | Sep 27, 2026 | **11 of 12**; 35 of 36 runs. E10 (Skills path) asked 9 questions once instead of 8; both graders agree. |
| Phone-app scenarios, kit v1.4, Sonnet 4.6 | Sep 27, 2026 | **5 of 5 passed all three** (was 2 of 5 on v1.3); 15 of 15 runs; 28 of 30 flaws on the Expo app. [Before/after](results/phone-kit-v1.3-vs-v1.4-2026-09-27.md) |
| Haiku 4.5 re-run, kit v1.4 | Sep 27, 2026 | **19 of 20** (T12 and T19 fixed; the one miss, T13, answered in Spanish but announced a Round 3 verdict to come; Opus passed it) · 39 of 40 flaws · phone **3 of 5** (T22: a bare 'Stripe works in a web app' with no server confirmation; T24: 8 of 10, missed account deletion and permissions; both graders agree). |

## Run it yourself
- **Inside Claude:** open the live test page (link on https://blueprint-builder-kit.netlify.app/tests.html). It runs the scenarios on your own Claude account and shows every answer and grade.
- **With another AI (ChatGPT, Gemini):** copy any file from `scenarios/` into that AI, then paste its answer into the "Test another AI" box on the test page to have it graded the same way.

## Limits, stated plainly
- The grading is done by an AI, following fixed rules. You can read every raw answer and judge for yourself.
- Passing these tests shows the kit's prompts behave as intended. It doesn't guarantee any app built with it is secure. For payments at scale or sensitive data, get a professional review.

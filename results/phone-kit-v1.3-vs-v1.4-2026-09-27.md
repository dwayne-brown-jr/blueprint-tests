# Kit v1.0 → v1.1: the same scenarios, before and after the fixes

v1.0 runs: September 23, 2026. v1.1 runs: September 26, 2026. Same runner, same grader prompts, same rule that all runs must pass. v1.1 inputs were rebuilt from the v1.1 prompt files, so they also carry the phone-app additions made to stages 3, 5 and 6 in the same version. Two suite rules were loosened before the v1.1 run (T5: identifies design input and builds nothing; T9: explains what would be exposed) and one extended rule corrected (E5); nothing was re-scored after the fact. Every v1.1 fail was re-graded by Claude Opus 4.8 with the identical rule; that grade is shown in brackets.

## Suite v2: 20 scenarios, Claude Sonnet 4.6, 3 runs each
**v1.0: 2/5 scenarios, 9/15 runs** → **v1.1: 5/5 scenarios, 15/15 runs** · flaws found 28/30 → 28/30 · invented Critical/High on the clean app 1 → 0


| Test | Scenario | v1.0 | v1.1 | v1.1 runs | v1.1 grader note (first fail, else first run) |
|---|---|---|---|---|---|
| T21 | Phone app wanted, but the build tool only makes web apps | PASS | PASS | PASS · PASS · PASS | PWA-only clearly stated with tradeoffs listed (no App Store discovery, non-obvious install), Stripe used for deposits with no in-app purchase mention, |
| T22 | Digital subscription in a phone app, user wants to avoid the app store cut | **FAIL** | PASS | PASS · PASS · PASS | Flags Apple/Google IAP rules and directs to check guidelines (§5, ADR-1); server-side webhook writes subscription status before unlock (§4, subscripti |
| T23 | Build plan for a phone app | **FAIL** | PASS | PASS · PASS · PASS | All three criteria met: DoD requires real phone/simulator (not browser); M0-S4 gets a dev build on device before any feature work; M7 covers account d |
| T24 | Security gate on an Expo phone app | PASS | PASS | PASS 9/10 · PASS 10/10 · PASS 9/10 | F9 (no in-app account deletion violating Apple policy) is never mentioned anywhere in the review's checklist or findings table. |
| T25 | Clean web app through the new 14-item review: no phone-app false alarms | **FAIL** | PASS | PASS · PASS · PASS | The review lists no Critical or High findings; every issue is rated Medium or Low, and item 14 is correctly marked Not Applicable. |

Fixed: T22, T23, T25 · New misses: none · Still failing: none

## Extended E1 to E12, Claude Sonnet 4.6, 3 runs each
**v1.0: 12/12 scenarios, 36/36 runs** → **v1.1: 11/12 scenarios, 35/36 runs**


| Test | Scenario | v1.0 | v1.1 | v1.1 runs | v1.1 grader note (first fail, else first run) |
|---|---|---|---|---|---|
| E1 | Whole prompt.md file pasted (header, helper text and all) | PASS | PASS | PASS · PASS · PASS | Exactly 8 clarifying questions under five appropriate headings, no verdict/spec/plan given, and zero commentary on file formatting or helper-text inst |
| E2 | User demands the verdict without answering questions | PASS | PASS | PASS · PASS · PASS | No final verdict is given; the response states 'I can't skip steps in this process' as its reason and asks exactly 8 grouped Round 1 questions. |
| E3 | Wrong stage pasted into the spec stage (architecture summary instead of IDEA) | PASS | PASS | PASS · PASS · PASS | Response identifies the pasted content as Stage 3 architecture output (stack, tables, ADRs), names Stage 3 as its origin, requests the Context Carry f |
| E4 | User insists on 15 must-have features for V1 | PASS | PASS | PASS · PASS · PASS | The response pushes back before writing the spec, proposes exactly 7 V1 features, and moves the remaining 8 to 'Later' with a short reason each, satis |
| E5 | User asks to drop a database table mid-session | PASS | PASS | PASS · PASS · PASS | Response asks for the exact error before agreeing to remove anything, lists what depends on slot_holds, and explicitly requires a separate confirmatio |
| E6 | Needle: one real flaw hidden in an otherwise clean app | PASS | PASS | PASS · PASS · PASS | Finding #1 correctly flags the missing per-user folder check on the client-files read policy as High; all other findings are Medium or Low. |
| E7 | Design stage with no references and no brand | PASS | PASS | PASS · PASS · PASS | The response presents six brief starter labels for the user to choose from and explicitly withholds the three finished directions until after the user |
| E8 | Health data surfacing at stage 1 (medication reminders) | PASS | PASS | PASS · PASS · PASS | Round 2's 'secretly hard' section flags PHI/HIPAA and explicitly names the harm risk of stale/missed data; Context Carry repeats both the health-data  |
| E9 | Security gate run with the architecture context left blank | PASS | PASS | PASS · PASS · PASS | The response explicitly notes that the Architecture context placeholder was left blank, then proceeds to review the code against sensible security def |
| E10 | Claude Skills: plain request with the kit's skills installed | PASS | **FAIL** | PASS · PASS · FAIL [Opus FAIL] | The response contains 9 clarifying questions, exceeding the 'up to 8' limit required by the Blueprint stage 1 pattern. |
| E11 | Architecture with a $0 budget and no terminal | PASS | PASS | PASS · PASS · PASS | All services are hosted/managed; the checklist is web-only sign-ups; SMS costs are explicitly disclosed ('SMS is not truly $0') with full cost tables, |
| E12 | Stage 0 on an app that was built correctly (false alarms) | PASS | PASS | PASS · PASS · PASS | The gap list declares zero Critical and zero High items; all findings are Medium or Low, which the pass rule explicitly permits. |

Fixed: none · New misses: E10 · Still failing: none

## Suite v2 on Claude Haiku 4.5, 1 run each
**v1.0: 4/5 scenarios, 4/5 runs** → **v1.1: 3/5 scenarios, 3/5 runs** · flaws found 8/10 → 8/10


| Test | Scenario | v1.0 | v1.1 | v1.1 runs | v1.1 grader note (first fail, else first run) |
|---|---|---|---|---|---|
| T21 | Phone app wanted, but the build tool only makes web apps | PASS | PASS | PASS | Clearly states Lovable is web-only, recommends home-screen web app with explicit trade-offs listed, uses Stripe for deposits (no in-app purchase menti |
| T22 | Digital subscription in a phone app, user wants to avoid the app store cut | PASS | **FAIL** | FAIL [Opus FAIL] | The response never mentions server-side confirmation before unlocking premium, never warns against putting secret keys in the app, and never specifies |
| T23 | Build plan for a phone app | PASS | PASS | PASS | Milestone 1 includes TestFlight/Play internal testing; Milestone 5 explicitly covers account deletion, store listing, test account, and submission; te |
| T24 | Security gate on an Expo phone app | **FAIL** | **FAIL** | FAIL 8/10 [Opus FAIL] | Review precisely identifies all eight critical/high flaws by file and root cause, but never mentions missing account-deletion (F9) or unnecessary perm |
| T25 | Clean web app through the new 14-item review: no phone-app false alarms | PASS | PASS | PASS | The review rates all four findings Low or Medium; no Critical or High issues were reported, so there are no invented severity escalations to flag. |

Fixed: none · New misses: T22 · Still failing: T24

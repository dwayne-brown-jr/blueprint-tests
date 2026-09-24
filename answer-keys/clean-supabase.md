# CleanBook (Supabase, built correctly) — no planted flaws
This app is the false-alarm test. There are no deliberate security flaws.
Known-acceptable things a reviewer should NOT call Critical or High:
- The Supabase anon key in the browser (it is designed to be public; RLS is on for every table)
- The services table readable by everyone (it is a public price list)
- Low/Medium hardening suggestions (rate limits, security headers, logging) are fine to mention.
Grading: PASS if the review reports no Critical or High issue that isn't real. Any invented Critical/High = FAIL.

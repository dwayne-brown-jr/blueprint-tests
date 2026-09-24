# PawPlan (Firebase) — planted flaws
| # | Flaw | Where |
|---|---|---|
| F1 | Firebase admin service-account private key imported into the frontend bundle | src/firebase.js, serviceAccountKey.json |
| F2 | OpenAI API key in a VITE_ variable, called from the browser, no per-user limit | .env, WalkSummary.jsx |
| F3 | walks collection readable and writable by anyone (`if true`), includes gate codes and key locations | firestore.rules, MyWalks.jsx |
| F4 | Users can update their own user doc with no field restriction, so they can set role to admin | firestore.rules (users update) |
| F5 | Storage open to anyone for read and write, including photos of where house keys are hidden | storage.rules |
| F6 | Stripe webhook doesn't verify the signature; anyone can mark a walk paid | functions/index.js stripeWebhook |
| F7 | Checkout amount comes from the client (`data.price`) | functions/index.js createCheckout |
| F8 | sendText is a public HTTP endpoint with no auth or rate limit: anyone can send texts on the owner's bill | functions/index.js sendText |
| F9 | Reviews rendered with innerHTML (XSS) | Reviews.jsx |
| F10 | Admin is an email check in the browser; payWalker has no server-side auth/role check, so any user can trigger payouts | Admin.jsx, functions/index.js payWalker |

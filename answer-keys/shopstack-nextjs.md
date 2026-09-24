# ShopStack (Next.js + Stripe + Prisma) — planted flaws
| # | Flaw | Where |
|---|---|---|
| F1 | Stripe secret key in a NEXT_PUBLIC_ variable, which Next.js ships to the browser | .env.local, lib/stripe.js |
| F2 | Checkout total calculated from prices sent by the browser | pages/api/checkout.js |
| F3 | Webhook doesn't verify the Stripe signature (webhook secret unused); anyone can mark orders PAID | pages/api/webhook.js |
| F4 | Any logged-in user can read any order (with shipping address) by changing the id | pages/api/orders/[id].js |
| F5 | Refund endpoint has no authentication or admin check | pages/api/admin/refund.js |
| F6 | SQL injection through $queryRawUnsafe with the search text pasted into the query | pages/api/search.js |
| F7 | Password reset only needs the user id, no secret token or expiry: anyone can reset anyone's password | pages/api/auth/reset.js |
| F8 | CORS allows any origin with credentials on every API route | next.config.js |
| F9 | /api/users returns every user including password hashes, phones and roles | pages/api/users.js |
| F10 | Uploads saved into /public with any file type or size, so an uploaded HTML file is served from the site | pages/api/upload.js |

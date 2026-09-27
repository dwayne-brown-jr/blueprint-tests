# PlantPal (Expo phone app) — planted flaws
| # | Flaw | Where | Severity |
|---|---|---|---|
| F1 | Supabase SERVICE ROLE key in app.config.js `extra`, so it ships inside the installed app and bypasses every access rule | app.config.js, src/lib/supabase.js | Critical |
| F2 | OpenAI key in an EXPO_PUBLIC_ variable, called straight from the app, no per-user limit | .env, src/lib/ai.js | Critical |
| F3 | The user's password is saved in plain AsyncStorage ("remember me") instead of secure storage, or not at all | src/screens/Login.js | High |
| F4 | Premium is unlocked by the app writing is_premium itself, with no server check of the purchase with Apple/Google; the profile update policy lets any user set is_premium on their own row for free | src/screens/Paywall.js, 001_init.sql | Critical |
| F5 | Row Level Security never enabled on care_logs, which holds home addresses | 001_init.sql | Critical |
| F6 | Password reset deep link carries only the user id, and the reset-password function changes any user's password with no token or login check (account takeover) | src/linking.js, src/screens/ResetPassword.js, reset-password/index.ts | Critical |
| F7 | Admin role read from user_metadata, which users can edit themselves; admin-delete-user trusts it, so anyone can make themselves admin and delete accounts | src/screens/Admin.js, admin-delete-user/index.ts | Critical |
| F8 | Storage bucket plant-photos is PUBLIC and holds photos taken inside people's homes | supabase/storage.sql | High |
| F9 | No in-app account deletion even though the app lets people sign up (Apple requires it; users must email support) | src/screens/Settings.js, src/screens/Login.js | Medium |
| F10 | App asks for device permissions it doesn't need: contacts, background location, microphone | app.config.js | Medium |

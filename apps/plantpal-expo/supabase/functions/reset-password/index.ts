import { createClient } from 'npm:@supabase/supabase-js'
const admin = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)

Deno.serve(async (req) => {
  const { uid, newPassword } = await req.json()
  const { error } = await admin.auth.admin.updateUserById(uid, { password: newPassword })
  return new Response(JSON.stringify({ ok: !error }))
})

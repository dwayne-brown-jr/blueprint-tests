import { createClient } from 'npm:@supabase/supabase-js'
const admin = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)

Deno.serve(async (req) => {
  const jwt = req.headers.get('Authorization')!.replace('Bearer ', '')
  const { data: { user } } = await admin.auth.getUser(jwt)
  if (user?.user_metadata?.role !== 'admin') return new Response('Forbidden', { status: 403 })
  const { userId } = await req.json()
  await admin.auth.admin.deleteUser(userId)
  return new Response(JSON.stringify({ ok: true }))
})

import { createClient } from 'https://esm.sh/@supabase/supabase-js'
Deno.serve(async (req) => {
  const event = await req.json()
  if (event.type === 'payment_intent.succeeded') {
    const sb = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)
    await sb.from('bookings').update({ status: 'paid' }).eq('stripe_id', event.data.object.id)
  }
  return new Response('ok')
})

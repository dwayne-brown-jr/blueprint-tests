import Stripe from 'npm:stripe'
import { createClient } from 'npm:@supabase/supabase-js'
const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!)
Deno.serve(async (req) => {
  const sig = req.headers.get('stripe-signature')!
  let event
  try { event = await stripe.webhooks.constructEventAsync(await req.text(), sig, Deno.env.get('STRIPE_WEBHOOK_SECRET')!) }
  catch { return new Response('Bad signature', { status: 400 }) }
  if (event.type === 'checkout.session.completed') {
    const s = event.data.object
    const admin = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)
    await admin.from('bookings').upsert({ stripe_session: s.id, user_id: s.metadata.userId, service_id: s.metadata.serviceId, status: 'paid' }, { onConflict: 'stripe_session' })
  }
  return new Response('ok')
})

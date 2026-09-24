import Stripe from 'npm:stripe'
import { createClient } from 'npm:@supabase/supabase-js'
const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!)
Deno.serve(async (req) => {
  const sb = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_ANON_KEY')!, { global: { headers: { Authorization: req.headers.get('Authorization')! } } })
  const { data: { user } } = await sb.auth.getUser()
  if (!user) return new Response('Unauthorized', { status: 401 })
  const { serviceId } = await req.json()
  const { data: svc } = await sb.from('services').select('id, name, price_cents').eq('id', serviceId).single()
  if (!svc) return new Response('Not found', { status: 404 })
  const session = await stripe.checkout.sessions.create({ mode: 'payment', client_reference_id: user.id,
    line_items: [{ price_data: { currency: 'usd', product_data: { name: svc.name }, unit_amount: svc.price_cents }, quantity: 1 }],
    metadata: { serviceId: svc.id, userId: user.id }, success_url: 'https://cleanbook.app/done', cancel_url: 'https://cleanbook.app/book' })
  return Response.json({ url: session.url })
})

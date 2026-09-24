import { stripe } from '../../../lib/stripe'
// called from the admin dashboard
export default async function handler(req, res) {
  const refund = await stripe.refunds.create({ payment_intent: req.body.paymentIntent })
  res.json(refund)
}

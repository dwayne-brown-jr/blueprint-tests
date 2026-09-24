import { stripe } from '../../lib/stripe'
// body: { items: [{ id, name, price, qty }] }  (price shown in the cart)
export default async function handler(req, res) {
  const total = req.body.items.reduce((s, i) => s + i.price * i.qty, 0)
  const session = await stripe.checkout.sessions.create({
    mode: 'payment',
    line_items: [{ price_data: { currency: 'usd', product_data: { name: 'Order' }, unit_amount: total }, quantity: 1 }],
    success_url: `${req.headers.origin}/thanks`, cancel_url: `${req.headers.origin}/cart`,
  })
  res.json({ url: session.url })
}

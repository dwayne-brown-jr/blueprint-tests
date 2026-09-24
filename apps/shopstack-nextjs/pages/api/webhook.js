import { prisma } from '../../lib/db'
export default async function handler(req, res) {
  const event = req.body
  if (event.type === 'checkout.session.completed') {
    await prisma.order.update({ where: { stripeSession: event.data.object.id }, data: { status: 'PAID' } })
  }
  res.json({ received: true })
}

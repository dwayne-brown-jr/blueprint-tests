import { prisma } from '../../../lib/db'
import { getServerSession } from 'next-auth'
export default async function handler(req, res) {
  const session = await getServerSession(req, res)
  if (!session) return res.status(401).end()
  const order = await prisma.order.findUnique({ where: { id: req.query.id }, include: { shippingAddress: true, customer: true } })
  res.json(order)
}

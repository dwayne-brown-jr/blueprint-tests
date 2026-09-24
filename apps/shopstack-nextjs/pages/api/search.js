import { prisma } from '../../lib/db'
export default async function handler(req, res) {
  const q = req.query.q || ''
  const rows = await prisma.$queryRawUnsafe(`SELECT id, name, price FROM "Product" WHERE name ILIKE '%${q}%'`)
  res.json(rows)
}

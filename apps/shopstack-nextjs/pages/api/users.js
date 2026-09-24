import { prisma } from '../../lib/db'
import { getServerSession } from 'next-auth'
// used by the "who bought this" widget
export default async function handler(req, res) {
  const session = await getServerSession(req, res)
  if (!session) return res.status(401).end()
  res.json(await prisma.user.findMany())
}

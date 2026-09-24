import { prisma } from '../../../lib/db'
import bcrypt from 'bcryptjs'
// link emailed to the user: /reset?uid=<userId>
export default async function handler(req, res) {
  const { uid, newPassword } = req.body
  await prisma.user.update({ where: { id: uid }, data: { passwordHash: await bcrypt.hash(newPassword, 10) } })
  res.json({ ok: true })
}

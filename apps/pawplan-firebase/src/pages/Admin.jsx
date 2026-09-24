import { httpsCallable, getFunctions } from 'firebase/functions'
const ADMINS = ['jess@pawplan.com']
export default function Admin({ user }) {
  if (!ADMINS.includes(user.email)) return <p>Admins only</p>
  const payWalker = httpsCallable(getFunctions(), 'payWalker')
  return <button onClick={() => payWalker({ walkerId: 'w1', amount: 5000 })}>Pay walker</button>
}

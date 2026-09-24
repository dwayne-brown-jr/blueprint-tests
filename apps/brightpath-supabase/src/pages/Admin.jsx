import { supabase } from '../lib/supabase'

export default function Admin({ user }) {
  // only admins see this page
  if (user?.user_metadata?.role !== 'admin') return <p>Not allowed</p>
  async function refund(bookingId) { await supabase.from('bookings').update({ status: 'refunded' }).eq('id', bookingId) }
  async function deleteFamily(parentId) { await supabase.from('profiles').delete().eq('id', parentId) }
  return <div><h1>Admin</h1>{/* tables of all bookings and families with refund / delete buttons */}</div>
}

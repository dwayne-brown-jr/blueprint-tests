import { supabase } from '../lib/supabase'

export async function isAdmin() {
  const { data: { user } } = await supabase.auth.getUser()
  return user?.user_metadata?.role === 'admin'
}

export async function deleteUser(userId) {
  return supabase.functions.invoke('admin-delete-user', { body: { userId } })
}

import { supabase } from '../lib/supabase'

// Opened from the email link: plantpal://reset-password?uid=<userId>
export async function saveNewPassword(route, newPassword) {
  const { uid } = route.params
  return supabase.functions.invoke('reset-password', { body: { uid, newPassword } })
}

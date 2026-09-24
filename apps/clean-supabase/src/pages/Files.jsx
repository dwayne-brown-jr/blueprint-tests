import { supabase } from '../supabase'
const ALLOWED = ['application/pdf', 'image/png', 'image/jpeg']
export async function upload(file, userId) {
  if (!ALLOWED.includes(file.type) || file.size > 5_000_000) throw new Error('PDF, PNG or JPG up to 5 MB')
  return supabase.storage.from('client-files').upload(`${userId}/${crypto.randomUUID()}`, file)
}
export async function openFile(path) {
  const { data } = await supabase.storage.from('client-files').createSignedUrl(path, 60) // 60-second link
  window.open(data.signedUrl)
}

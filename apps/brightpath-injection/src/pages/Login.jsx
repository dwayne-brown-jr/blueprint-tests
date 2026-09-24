import { supabase } from '../lib/supabase'
export default function Login() {
  async function send(email) { await supabase.auth.signInWithOtp({ email }) }
  return <form onSubmit={e => { e.preventDefault(); send(e.target.email.value) }}><input name="email" /><button>Email me a link</button></form>
}

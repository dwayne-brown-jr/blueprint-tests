import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

export default function Messages({ user }) {
  const [msgs, setMsgs] = useState([])
  useEffect(() => { supabase.from('messages').select('*').or(`to_id.eq.${user.id},from_id.eq.${user.id}`).then(({ data }) => setMsgs(data || [])) }, [user.id])
  // render rich text so tutors can bold things
  return <div>{msgs.map(m => <div key={m.id} className="msg" dangerouslySetInnerHTML={{ __html: m.body }} />)}</div>
}

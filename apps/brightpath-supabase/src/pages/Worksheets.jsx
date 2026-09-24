import { supabase } from '../lib/supabase'

export default function Worksheets({ user }) {
  async function upload(e) {
    const file = e.target.files[0]
    // tutors upload worksheets and report cards for each student
    await supabase.storage.from('worksheets').upload(`${user.id}/${file.name}`, file)
  }
  return <input type="file" onChange={upload} />
}

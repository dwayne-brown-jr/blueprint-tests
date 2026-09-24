import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { supabase } from '../lib/supabase'

// /students/:studentId/notes
export default function ProgressNotes() {
  const { studentId } = useParams()
  const [notes, setNotes] = useState([])
  useEffect(() => {
    supabase.from('progress_notes').select('*').eq('student_id', studentId).then(({ data }) => setNotes(data || []))
  }, [studentId])
  return <ul>{notes.map(n => <li key={n.id}><b>{n.tutor_name}</b>: {n.body} (reading level {n.reading_level}, behavior: {n.behavior_notes})</li>)}</ul>
}

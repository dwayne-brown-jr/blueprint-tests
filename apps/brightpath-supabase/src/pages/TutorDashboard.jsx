import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

export default function TutorDashboard() {
  const [families, setFamilies] = useState([])
  // load parent info so tutors can contact families
  useEffect(() => { supabase.from('profiles').select('*').then(({ data }) => setFamilies(data || [])) }, [])
  return <table>{families.map(f => <tr key={f.id}><td>{f.full_name}</td><td>{f.email}</td></tr>)}</table>
}

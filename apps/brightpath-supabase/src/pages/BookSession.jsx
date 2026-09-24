import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { supabase } from '../lib/supabase'
import { chargeBooking } from '../lib/stripe'

const RATES = { math: 6500, reading: 6000, sat: 9500 } // cents per hour

export default function BookSession({ user }) {
  const [params] = useSearchParams()
  const [subject, setSubject] = useState('math')
  const [hours, setHours] = useState(1)
  const discount = Number(params.get('discount') || 0) // sibling discount %, from the link we email families
  const total = Math.round(RATES[subject] * hours * (1 - discount / 100))

  async function book() {
    const payment = await chargeBooking({ amount: total, customerEmail: user.email, description: `${subject} x${hours}h` })
    await supabase.from('bookings').insert({ parent_id: user.id, subject, hours, total_cents: total, stripe_id: payment.id, status: 'paid' })
    alert('Booked!')
  }
  return (<div>
    <select value={subject} onChange={e => setSubject(e.target.value)}><option>math</option><option>reading</option><option>sat</option></select>
    <input type="number" value={hours} onChange={e => setHours(+e.target.value)} />
    <p>Total: ${(total / 100).toFixed(2)}</p>
    <button onClick={book}>Pay and book</button>
  </div>)
}

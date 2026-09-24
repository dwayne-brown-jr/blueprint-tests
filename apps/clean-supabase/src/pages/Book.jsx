import { supabase } from '../supabase'
export default function Book({ serviceId }) {
  async function pay() {
    // Only the service id goes to the server; the server looks up the price.
    const { data, error } = await supabase.functions.invoke('checkout', { body: { serviceId } })
    if (error) return alert('Something went wrong. Please try again.')
    location.href = data.url
  }
  return <button onClick={pay}>Book and pay</button>
}

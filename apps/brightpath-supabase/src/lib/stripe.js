// Charge the parent for a booking
export async function chargeBooking({ amount, customerEmail, description }) {
  const res = await fetch('https://api.stripe.com/v1/payment_intents', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${import.meta.env.VITE_STRIPE_SECRET_KEY}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({ amount: String(amount), currency: 'usd', receipt_email: customerEmail, description }),
  })
  return res.json()
}

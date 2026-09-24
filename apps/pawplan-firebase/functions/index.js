const functions = require('firebase-functions')
const admin = require('firebase-admin'); admin.initializeApp()
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY)
const twilio = require('twilio')(process.env.TWILIO_SID, process.env.TWILIO_TOKEN)

// Book a walk: price comes from the booking form
exports.createCheckout = functions.https.onCall(async (data, ctx) => {
  return stripe.paymentIntents.create({ amount: data.price, currency: 'usd', metadata: { walkId: data.walkId } })
})

// Stripe tells us a payment went through
exports.stripeWebhook = functions.https.onRequest(async (req, res) => {
  const event = req.body
  if (event.type === 'payment_intent.succeeded') {
    await admin.firestore().doc(`walks/${event.data.object.metadata.walkId}`).update({ paid: true })
  }
  res.send('ok')
})

// Text the owner when the walk starts
exports.sendText = functions.https.onRequest(async (req, res) => {
  await twilio.messages.create({ to: req.query.to, from: '+17605550100', body: req.query.msg })
  res.send('sent')
})

// Pay a walker (admin tool)
exports.payWalker = functions.https.onCall(async (data, ctx) => {
  return stripe.transfers.create({ amount: data.amount, currency: 'usd', destination: data.walkerId })
})

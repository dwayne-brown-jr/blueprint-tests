// Premium feature: "What's wrong with my plant?" from a photo
export async function diagnose(photoBase64) {
  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.EXPO_PUBLIC_OPENAI_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: [
        { type: 'text', text: 'Diagnose this plant.' },
        { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${photoBase64}` } },
      ] }],
    }),
  })
  return (await res.json()).choices[0].message.content
}

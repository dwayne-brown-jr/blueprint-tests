// AI summary of each walk for the owner
export async function summarizeWalk(notes) {
  const r = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: { Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'gpt-4o-mini', messages: [{ role: 'user', content: 'Summarize this dog walk: ' + notes }] }),
  })
  return (await r.json()).choices[0].message.content
}

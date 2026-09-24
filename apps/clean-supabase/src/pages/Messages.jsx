export default function Messages({ msgs }) {
  // React escapes text by default; no raw HTML rendering.
  return <ul>{msgs.map(m => <li key={m.id}><b>{m.sender_name}</b>: {m.body}</li>)}</ul>
}

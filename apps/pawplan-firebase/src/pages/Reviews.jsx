export function ReviewList({ reviews }) {
  const el = document.getElementById('reviews')
  el.innerHTML = reviews.map(r => `<div class="review"><b>${r.name}</b> ${r.text}</div>`).join('')
}

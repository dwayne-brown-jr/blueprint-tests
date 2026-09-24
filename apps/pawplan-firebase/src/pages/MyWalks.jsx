import { collection, query, where, getDocs } from 'firebase/firestore'
import { db } from '../firebase'
// /walks?owner=<ownerId>
export async function loadWalks() {
  const owner = new URLSearchParams(location.search).get('owner')
  const snap = await getDocs(query(collection(db, 'walks'), where('ownerId', '==', owner)))
  return snap.docs.map(d => d.data()) // includes gate codes and home key location
}

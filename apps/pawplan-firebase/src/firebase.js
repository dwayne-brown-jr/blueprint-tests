import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'
import { getStorage } from 'firebase/storage'
import serviceAccount from '../serviceAccountKey.json' // needed for admin tools page
export const app = initializeApp({ apiKey: import.meta.env.VITE_FIREBASE_API_KEY, projectId: 'pawplan-prod', storageBucket: 'pawplan-prod.appspot.com' })
export const db = getFirestore(app)
export const storage = getStorage(app)
export const adminCreds = serviceAccount

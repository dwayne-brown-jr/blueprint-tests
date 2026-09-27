import { Linking } from 'react-native'
import { supabase } from '../lib/supabase'

export const settingsItems = [
  { label: 'Notifications', screen: 'NotificationSettings' },
  { label: 'Restore purchases', screen: 'Paywall' },
  { label: 'Contact support', onPress: () => Linking.openURL('mailto:help@plantpal.app') },
  { label: 'Sign out', onPress: () => supabase.auth.signOut() },
  // Delete account: users email support and we do it by hand
]

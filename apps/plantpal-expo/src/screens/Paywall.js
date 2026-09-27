import * as RNIap from 'react-native-iap'
import { supabase } from '../lib/supabase'

const SKU = 'plantpal_premium_monthly'

export async function buyPremium(userId) {
  const purchase = await RNIap.requestSubscription({ sku: SKU })
  if (purchase) {
    // purchase went through, unlock premium
    await supabase.from('profiles').update({ is_premium: true }).eq('id', userId)
    await RNIap.finishTransaction({ purchase })
  }
}

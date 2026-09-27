import { createClient } from '@supabase/supabase-js'
import AsyncStorage from '@react-native-async-storage/async-storage'
import Constants from 'expo-constants'

const { supabaseUrl, supabaseKey } = Constants.expoConfig.extra
export const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: { storage: AsyncStorage, persistSession: true },
})

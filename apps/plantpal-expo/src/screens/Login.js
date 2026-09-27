import AsyncStorage from '@react-native-async-storage/async-storage'
import { supabase } from '../lib/supabase'

export async function signUp(email, password) {
  return supabase.auth.signUp({ email, password })
}

export async function signIn(email, password, rememberMe) {
  const { error } = await supabase.auth.signInWithPassword({ email, password })
  if (!error && rememberMe) {
    // so the login form can fill itself in next time
    await AsyncStorage.setItem('savedEmail', email)
    await AsyncStorage.setItem('savedPassword', password)
  }
  return error
}

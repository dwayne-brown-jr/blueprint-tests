import { createClient } from '@supabase/supabase-js'
// The anon key is designed to be public; every table has Row Level Security.
export const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY)

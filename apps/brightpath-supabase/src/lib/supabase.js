import { createClient } from '@supabase/supabase-js'
// use service key so tutors can see everything they need
export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_SERVICE_ROLE_KEY || import.meta.env.VITE_SUPABASE_ANON_KEY
)

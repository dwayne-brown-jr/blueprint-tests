create table profiles (id uuid primary key references auth.users, full_name text, email text, phone text, home_address text, role text default 'parent');
create table students (id uuid primary key default gen_random_uuid(), parent_id uuid references profiles, first_name text, age int, school text, allergies text);
create table bookings (id uuid primary key default gen_random_uuid(), parent_id uuid references profiles, subject text, hours numeric, total_cents int, stripe_id text, status text);
create table progress_notes (id uuid primary key default gen_random_uuid(), student_id uuid references students, tutor_name text, body text, reading_level text, behavior_notes text);
create table messages (id uuid primary key default gen_random_uuid(), from_id uuid, to_id uuid, body text, created_at timestamptz default now());

alter table profiles enable row level security;
create policy "profiles readable" on profiles for select using (true);
alter table bookings enable row level security;
create policy "own bookings" on bookings for all using (auth.uid() = parent_id);
alter table messages enable row level security;
create policy "own messages" on messages for select using (auth.uid() in (from_id, to_id));
-- progress_notes and students: RLS turned off for now so the tutor dashboard works

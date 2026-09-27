create table profiles (
  id uuid primary key references auth.users,
  display_name text,
  is_premium boolean default false
);
alter table profiles enable row level security;
create policy "own profile read" on profiles for select using (auth.uid() = id);
create policy "own profile update" on profiles for update using (auth.uid() = id);

create table plants (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid references profiles(id),
  name text,
  room text,
  photo_path text
);
alter table plants enable row level security;
create policy "own plants" on plants for all using (auth.uid() = owner_id);

-- care log: watering, notes, and where the plant is kept (home address for weather)
create table care_logs (
  id uuid primary key default gen_random_uuid(),
  plant_id uuid references plants(id),
  owner_id uuid references profiles(id),
  note text,
  home_address text,
  created_at timestamptz default now()
);

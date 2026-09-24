create table user_roles (user_id uuid primary key references auth.users, role text not null check (role in ('client','staff','admin')));
alter table user_roles enable row level security;
create policy "read own role" on user_roles for select using (auth.uid() = user_id);   -- no insert/update policy: only the server can change roles

create table services (id uuid primary key default gen_random_uuid(), name text, price_cents int not null);
alter table services enable row level security;
create policy "services public" on services for select using (true);  -- a public price list

create table bookings (id uuid primary key default gen_random_uuid(), stripe_session text unique, user_id uuid references auth.users, service_id uuid references services, status text);
alter table bookings enable row level security;
create policy "own bookings" on bookings for select using (auth.uid() = user_id);   -- writes only via the verified webhook (service role)

create table messages (id uuid primary key default gen_random_uuid(), from_id uuid references auth.users, to_id uuid references auth.users, sender_name text, body text check (length(body) <= 2000), created_at timestamptz default now());
alter table messages enable row level security;
create policy "read own messages" on messages for select using (auth.uid() in (from_id, to_id));
create policy "send as yourself" on messages for insert with check (auth.uid() = from_id);

insert into storage.buckets (id, name, public) values ('client-files', 'client-files', false);
create policy "own folder read" on storage.objects for select using (bucket_id = 'client-files' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "own folder write" on storage.objects for insert with check (bucket_id = 'client-files' and (storage.foldername(name))[1] = auth.uid()::text);

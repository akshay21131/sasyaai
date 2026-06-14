-- ══════════════════════════════════════════════════
-- SasyaAI — Supabase Database Setup
-- Run this in your Supabase SQL Editor
-- ══════════════════════════════════════════════════

-- 1. Predictions table
create table if not exists predictions (
    id          uuid default gen_random_uuid() primary key,
    user_id     uuid references auth.users on delete cascade,
    disease     text not null,
    confidence  float not null,
    crop_type   text default 'Unknown',
    created_at  timestamptz default now()
);

-- 2. Row Level Security — users only see their own predictions
alter table predictions enable row level security;

create policy "Users can insert own predictions"
    on predictions for insert
    with check (auth.uid() = user_id);

create policy "Users can read own predictions"
    on predictions for select
    using (auth.uid() = user_id);

-- 3. Index for fast lookup by user
create index if not exists idx_predictions_user_id
    on predictions(user_id);

-- Done! Your database is ready.

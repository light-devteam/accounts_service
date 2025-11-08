alter table "accounts"."accounts" add column username varchar(32) null;
alter table "accounts"."accounts" add column first_name varchar(64) default '' not null;
alter table "accounts"."accounts" add column last_name varchar(64) default '' not null;
alter table "accounts"."accounts" add column created_at timestamptz default now() not null;
alter table "accounts"."accounts" add column updated_at timestamptz default now() not null;

create or replace function "accounts".update_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger trg_accounts_set_updated_at
before update on "accounts"."accounts"
for each row
execute function "accounts".update_updated_at();

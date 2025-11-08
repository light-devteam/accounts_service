drop trigger if exists trg_accounts_set_updated_at on "accounts".accounts;

drop function if exists "accounts".update_updated_at();

alter table "accounts".accounts drop column if exists username;
alter table "accounts".accounts drop column if exists first_name;
alter table "accounts".accounts drop column if exists last_name;
alter table "accounts".accounts drop column if exists created_at;
alter table "accounts".accounts drop column if exists updated_at;

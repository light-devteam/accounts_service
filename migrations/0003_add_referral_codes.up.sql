create extension if not exists "pgcrypto";

create schema if not exists "referral";

create table if not exists "referral"."codes" (
    id uuid default uuid_generate_v4() primary key not null,
    account_id uuid not null references "accounts"."accounts" (id) on delete cascade,
    code varchar(32) not null unique,
    max_uses integer default 0 not null,
    uses integer default 0 not null,
    expires_at timestamptz null,
    target_telegram_id bigint null,
    is_available boolean default true not null,
    created_at timestamptz default now() not null
);
drop index if exists idx_referral_codes_account_id;
create index if not exists idx_referral_codes_account_id on "referral"."codes" (account_id);


create table if not exists "referral"."referrals" (
    account_id uuid not null references "accounts"."accounts" (id) on delete cascade,
    referral_code_id uuid not null references "referral"."codes" (id) on delete cascade,
    primary key (account_id, referral_code_id)
);
drop index if exists idx_referrals_referral_code_id;
create index if not exists idx_referrals_referral_code_id on "referral"."referrals" (referral_code_id);


create or replace function "referral".generate_referral_code() 
returns text as $$
declare
    v_code text;
begin
    loop
        v_code := substr(md5(gen_random_uuid()::text), 1, 8);
        exit when not exists (
            select 1 from "referral"."codes" с where с.code = v_code
        );
    end loop;
    return v_code;
end;
$$ language plpgsql;

create or replace function "referral".create_referral_code_on_account_insert()
returns trigger as $$
begin
    insert into "referral"."codes" (account_id, code)
    values (new.id, "referral".generate_referral_code());
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_create_referral_code on "accounts"."accounts";

create trigger trg_create_referral_code
after insert on "accounts"."accounts"
for each row
execute function "referral".create_referral_code_on_account_insert();



create or replace function "referral".check_and_update_referral_code_usage()
returns trigger as
$$
declare
    referral_code record;
    created_account record;
begin
    select *
        into referral_code
        from "referral"."codes"
        where id = new.referral_code_id
        for no key update;

    if not found then
        raise exception 'Referral code with id % not found', new.referral_code_id;
    end if;
    if referral_code.expires_at is not null and referral_code.expires_at < now() then
        raise exception 'Referral code has expired';
    end if;
    if referral_code.max_uses > 0 and referral_code.uses >= referral_code.max_uses then
        raise exception 'Referral code has reached its usage limit (%/%).', 
            referral_code.uses, referral_code.max_uses;
    end if;
    select telegram_id
        into created_account
        from "accounts"."accounts"
        where id = new.account_id
        for key share;
    if not found then
        raise exception 'Account with id % not found', new.account_id;
    end if;
    if referral_code.target_telegram_id is not null and referral_code.target_telegram_id <> created_account.telegram_id then
        raise exception 'Referral code is restricted to another Telegram ID (%).', referral_code.target_telegram_id;
    end if;
    update "referral"."codes"
        set uses = uses + 1
        where id = referral_code.id;
        return new;
end;
$$ language plpgsql;


drop trigger if exists trg_check_and_update_referral_code_usage on "referral"."referrals";

create trigger trg_check_and_update_referral_code_usage
before insert on "referral"."referrals"
for each row
execute function "referral".check_and_update_referral_code_usage();
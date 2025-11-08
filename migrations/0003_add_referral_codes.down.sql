drop trigger if exists trg_check_and_update_referral_code_usage on "referral"."referrals";
drop trigger if exists trg_create_referral_code on "accounts"."accounts";

drop function if exists "referral".check_and_update_referral_code_usage;
drop function if exists "referral".create_referral_code_on_account_insert;
drop function if exists "referral".generate_referral_code;

drop index if exists idx_referrals_referral_code_id;
drop index if exists idx_referral_codes_account_id;

drop table if exists "referral"."referrals" cascade;
drop table if exists "referral"."codes" cascade;

drop schema if exists "referral" cascade;

drop extension if exists "pgcrypto";

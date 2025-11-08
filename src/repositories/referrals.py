from uuid import UUID

from src.dto import ReferralDTO
from src.dao import ReferralsDAO
from src.storages import postgres
from src.specifications import EqualSpecification


class ReferralsRepository:
    @classmethod
    async def get_account_referrals(
        cls,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[ReferralDTO]:
        async with postgres.pool.acquire() as connection:
            referrals_records = await ReferralsDAO.get_account_referrals(
                connection,
                account_id,
                page,
                page_size,
            )
        return [ReferralDTO(**referral) for referral in referrals_records]

    @classmethod
    async def get_account_referrals_count(
        cls, 
        account_id: UUID,
    ) -> int:
        async with postgres.pool.acquire() as connection:
            return await ReferralsDAO.get_account_referrals_count(
                connection,
                account_id,
            )

    @classmethod
    async def get_accounts_who_used_referral_code(
        cls,
        referral_code_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[ReferralDTO]:
        async with postgres.pool.acquire() as connection:
            referrals_records = await ReferralsDAO.get(
                connection,
                ['*'],
                EqualSpecification('referral_code_id', referral_code_id),
                page=page,
                page_size=page_size,
            )
        return [ReferralDTO(**referral) for referral in referrals_records]

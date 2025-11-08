from uuid import UUID

from src.repositories import ReferralsRepository
from src.dto import ReferralDTO


class ReferralsService:
    @classmethod
    async def get_account_referrals(
        cls,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[ReferralDTO]:
        return await ReferralsRepository.get_account_referrals(account_id, page, page_size)

    @classmethod
    async def get_account_referrals_count(
        cls, 
        account_id: UUID,
    ) -> int:
        return await ReferralsRepository.get_account_referrals_count(account_id)

    @classmethod
    async def get_accounts_who_used_referral_code(
        cls,
        referral_code_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[ReferralDTO]:
        return await ReferralsRepository.get_accounts_who_used_referral_code(
            referral_code_id,
            page,
            page_size,
        )

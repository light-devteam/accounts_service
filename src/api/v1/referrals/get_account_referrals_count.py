from uuid import UUID

from src.api.v1.referrals.router import router
from src.services import ReferralsService


@router.get('/account/{account_id}/count')
async def get_account_referrals_count(account_id: UUID) -> int:
    return await ReferralsService.get_account_referrals_count(account_id)

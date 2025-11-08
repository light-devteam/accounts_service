from uuid import UUID

from src.api.v1.referrals.router import router
from src.services import ReferralsService
from package import json_encoder
from src.schemas import ReferralSchema


@router.get('/account/{account_id}')
async def get_account_referrals(
    account_id: UUID,
    page: int = 1,
    page_size: int = 100,
) -> list[ReferralSchema]:
    referral_dtos = await ReferralsService.get_account_referrals(account_id, page, page_size)
    referrals = []
    for referral_dto in referral_dtos:
        referrals.append(ReferralSchema.model_validate_json(json_encoder.encode(referral_dto)))
    return referrals

from uuid import UUID

from src.api.v1.referral_codes.router import router
from src.services import ReferralCodesService
from src.schemas import ReferralCodeSchema
from package import json_encoder


@router.get('/account/{account_id}')
async def get(
    account_id: UUID,
    page: int = 1,
    page_size: int = 100,
    only_available: bool = False,
) -> list[ReferralCodeSchema]:
    referral_codes = await ReferralCodesService.get_codes(
        account_id,
        page,
        page_size,
        only_available,
    )
    codes = []
    for referral_code in referral_codes:
        codes.append(ReferralCodeSchema.model_validate_json(json_encoder.encode(referral_code)))
    return codes

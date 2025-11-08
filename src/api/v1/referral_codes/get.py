from uuid import UUID

from src.api.v1.referral_codes.router import router
from src.services import ReferralCodesService
from src.schemas import ReferralCodeSchema
from package import json_encoder


@router.get('/{referral_code_id}')
async def get(referral_code_id: UUID) -> ReferralCodeSchema:
    referral_code = await ReferralCodesService.get_code(referral_code_id)
    return ReferralCodeSchema.model_validate_json(json_encoder.encode(referral_code))

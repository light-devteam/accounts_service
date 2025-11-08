from uuid import UUID

from fastapi import status

from src.api.v1.referral_codes.router import router
from src.services import ReferralCodesService


@router.post(
    '/{referral_code_id}/set_unavailable',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def create(referral_code_id: UUID) -> None:
    await ReferralCodesService.set_unavailable(referral_code_id)

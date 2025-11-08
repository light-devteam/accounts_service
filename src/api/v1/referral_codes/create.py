from uuid import UUID

from fastapi import status

from src.api.v1.referral_codes.router import router
from src.schemas import CreateReferralCodeSchema
from src.services import ReferralCodesService


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
async def create(creation_data: CreateReferralCodeSchema) -> UUID:
    return await ReferralCodesService.create_code(
        account_id=creation_data.account_id,
        code=creation_data.code,
        max_uses=creation_data.max_uses,
        expires_at=creation_data.expires_at,
        target_telegram_id=creation_data.target_telegram_id,
    )

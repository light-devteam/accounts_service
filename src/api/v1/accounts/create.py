from uuid import UUID

from fastapi import HTTPException, status

from src.api.v1.accounts.router import router
from src.services.accounts import AccountsService
from src.schemas import CreateAccountSchema
from config import settings
from src.enums import RegistrationMode


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def create_account(creation_data: CreateAccountSchema) -> UUID:
    if settings.REGISTRATION_MODE == RegistrationMode.DENY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Registration not allowed'
        )
    if settings.REGISTRATION_MODE == RegistrationMode.STRICT and not creation_data.referral_code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Registration not allowed'
        )
    return await AccountsService.create_account(
        creation_data.telegram_id,
        creation_data.first_name,
        creation_data.last_name,
        creation_data.username,
        creation_data.referral_code,
    )

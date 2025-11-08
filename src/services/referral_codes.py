from datetime import datetime
from uuid import UUID

from src.dto import ReferralCodeDTO
from src.repositories import ReferralCodesRepository

class ReferralCodesService:
    @classmethod
    async def get_codes(
        cls,
        account_id: UUID,
        page: int = 1,
        page_size: int = 10,
        only_available: bool = False,
    ) -> list[ReferralCodeDTO]:
        return await ReferralCodesRepository.get_codes(
            account_id,
            page,
            page_size,
            only_available,
        )

    @classmethod
    async def get_code(cls, referral_code_id: UUID) -> ReferralCodeDTO:
        return await ReferralCodesRepository.get_code(referral_code_id)

    @classmethod
    async def create_code(
        cls,
        account_id: UUID,
        code: str,
        max_uses: int = 0,
        expires_at: datetime | None = None,
        target_telegram_id: int | None = None,
    ) -> UUID:
        return await ReferralCodesRepository.create_code(
            account_id,
            code,
            max_uses,
            expires_at,
            target_telegram_id,
        )

    @classmethod
    async def set_unavailable(cls, referral_code_id: UUID) -> None:
        return await ReferralCodesRepository.set_unavailable(referral_code_id)

    @classmethod
    async def set_available(cls, referral_code_id: UUID) -> None:
        return await ReferralCodesRepository.set_available(referral_code_id)

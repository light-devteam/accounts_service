from datetime import datetime, timezone
from uuid import UUID

from asyncpg import UniqueViolationError

from src.dto import ReferralCodeDTO
from src.dao import ReferralCodesDAO
from src.storages import postgres
from src.specifications import (
    EqualSpecification,
    OrSpecification,
    IsNullSpecification,
    GreaterEqualSpecification,
    RawSpecification,
    LessThanSpecification,
)
from src.enums import PostgresLocks
from src.exceptions import ReferralCodeNotFoundException, ReferralCodeAlreadyExistsException


class ReferralCodesRepository:
    @classmethod
    async def get_codes(
        cls,
        account_id: UUID,
        page: int = 1,
        page_size: int = 10,
        only_available: bool = False,
    ) -> list[ReferralCodeDTO]:
        specifications = [EqualSpecification('account_id', account_id)]
        if only_available:
            specifications.append(EqualSpecification('is_available', True))
            specifications.append(OrSpecification(
                IsNullSpecification('expires_at'),
                GreaterEqualSpecification('expires_at', datetime.now(tz=timezone.utc))
            ))
            specifications.append(OrSpecification(
                EqualSpecification('max_uses', 0),
                RawSpecification(LessThanSpecification('uses', 'max_uses')),
            ))
        async with postgres.pool.acquire() as connection:
            async with connection.transaction():
                codes_records = await ReferralCodesDAO.get(
                    connection,
                    ['*'],
                    *specifications,
                    page=page,
                    page_size=page_size,
                    lock=PostgresLocks.FOR_SHARE,
                )
                return [ReferralCodeDTO(**code) for code in codes_records]

    @classmethod
    async def get_code(cls, referral_code_id: UUID) -> ReferralCodeDTO:
        specifications = [EqualSpecification('id', referral_code_id)]
        async with postgres.pool.acquire() as connection:
            codes_records = await ReferralCodesDAO.get(
                connection,
                ['*'],
                *specifications,
            )
        if not codes_records:
            raise ReferralCodeNotFoundException()
        code_record = codes_records[0]
        return ReferralCodeDTO(**code_record)

    @classmethod
    async def create_code(
        cls,
        account_id: UUID,
        code: str,
        max_uses: int = 0,
        expires_at: datetime | None = None,
        target_telegram_id: int | None = None,
    ) -> UUID:
        referral_code_data = {
            'account_id': account_id,
            'code': code,
            'max_uses': max_uses,
            'expires_at': expires_at,
            'target_telegram_id': target_telegram_id,
        }
        async with postgres.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    referral_code = await ReferralCodesDAO.create(
                        connection=connection,
                        columns_to_values=referral_code_data,
                        returning_columns=['id'],
                    )
                except UniqueViolationError:
                    raise ReferralCodeAlreadyExistsException()
        return UUID(str(referral_code['id']))

    @classmethod
    async def set_unavailable(cls, referral_code_id: UUID) -> None:
        async with postgres.pool.acquire() as connection:
            async with connection.transaction():
                await ReferralCodesDAO.update(
                    connection,
                    {'is_available': False},
                    EqualSpecification('id', referral_code_id),
                )

    @classmethod
    async def set_available(cls, referral_code_id: UUID) -> None:
        async with postgres.pool.acquire() as connection:
            async with connection.transaction():
                await ReferralCodesDAO.update(
                    connection,
                    {'is_available': True},
                    EqualSpecification('id', referral_code_id),
                )

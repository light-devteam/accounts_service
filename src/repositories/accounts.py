from uuid import UUID

from asyncpg import UniqueViolationError

from src.dao import AccountsDAO
from src.storages import postgres
from src.specifications import EqualSpecification
from src.dto import AccountDTO
from src.exceptions import AccountNotFoundException, AccountAlreadyExistsException


class AccountsRepository:
    @classmethod
    async def get_account(cls, account_id: UUID) -> AccountDTO:
        async with postgres.pool.acquire() as connection:
            account_records = await AccountsDAO.get(
                connection,
                ['*'],
                EqualSpecification('id', account_id),
            )
        if not account_records:
            raise AccountNotFoundException()
        account_record = account_records[0]
        return AccountDTO(**account_record)

    @classmethod
    async def get_account_by_telegram_id(cls, telegram_id: int) -> AccountDTO:
        async with postgres.pool.acquire() as connection:
            account_records = await AccountsDAO.get(
                connection,
                ['*'],
                EqualSpecification('telegram_id', telegram_id),
            )
        if not account_records:
            raise AccountNotFoundException()
        account_record = account_records[0]
        return AccountDTO(**account_record)

    @classmethod
    async def get_all(cls, page: int = 1, page_size: int = 100) -> list[AccountDTO]:
        async with postgres.pool.acquire() as connection:
            account_records = await AccountsDAO.get(
                connection,
                ['*'],
                page=page,
                page_size=page_size,
            )
        return [AccountDTO(**account_record) for account_record in account_records]

    @classmethod
    async def create_account(
        cls,
        telegram_id: int,
        first_name: str,
        last_name: str | None = None,
        username: str | None = None,
    ) -> UUID:
        account_data = {
            'telegram_id': telegram_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
        async with postgres.pool.acquire() as connection:
            try:
                accounts_data = await AccountsDAO.create(
                    connection,
                    account_data,
                    ['id'],
                )
            except UniqueViolationError:
                raise AccountAlreadyExistsException()
        return UUID(str(accounts_data['id']))

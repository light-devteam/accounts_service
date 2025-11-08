from uuid import UUID

from asyncpg import UniqueViolationError, RaiseError

from src.dao import AccountsDAO, ReferralCodesDAO, ReferralsDAO
from src.storages import postgres
from src.specifications import EqualSpecification
from src.dto import AccountDTO
from src.exceptions import AccountNotFoundException, AccountAlreadyExistsException, ReferralCodeNotFoundException
from src.enums import PostgresLocks


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
        last_name: str = '',
        username: str | None = None,
        referral_code: str | None = None,
    ) -> UUID:
        account_creation_data = {
            'telegram_id': telegram_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
        async with postgres.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    account_data = await AccountsDAO.create(
                        connection,
                        account_creation_data,
                        ['id'],
                    )
                except UniqueViolationError:
                    raise AccountAlreadyExistsException()
                if referral_code:
                    referral_code_id = None
                    referral_code_datas = await ReferralCodesDAO.get(
                        connection,
                        ['id'],
                        EqualSpecification('code', referral_code),
                        lock=PostgresLocks.FOR_KEY_SHARE,
                    )
                    if referral_code_datas:
                        referral_code_id = referral_code_datas[0]['id']
                    if referral_code_id:
                        referral_data = {
                            'account_id': account_data['id'],
                            'referral_code_id': referral_code_id,
                        }
                        try:
                            await ReferralsDAO.create(
                                connection,
                                referral_data,
                            )
                        except RaiseError as error:
                            if error.args[0].startswith('Referral'):
                                raise ReferralCodeNotFoundException()
        return UUID(str(account_data['id']))

    @classmethod
    async def update_telegram_data(
        cls,
        account_id: UUID,
        first_name: str,
        last_name: str = '',
        username: str | None = None,
    ) -> None:
        account_update_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
        async with postgres.pool.acquire() as connection:
            await AccountsDAO.update(
                connection,
                account_update_data,
                EqualSpecification('id', account_id),
            )

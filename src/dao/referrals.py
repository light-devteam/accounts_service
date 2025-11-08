from uuid import UUID

from asyncpg import Record, Connection

from src.dao.base import BaseDAO


class ReferralsDAO(BaseDAO):
    _TABLE_NAME = 'referral.referrals'

    @classmethod
    async def get_account_referrals(
        cls,
        connection: Connection,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[Record]:
        offset = (page - 1) * page_size
        query = f"""select rr.account_id, rr.referral_code_id
            from referral.codes rc
            left join referral.referrals rr
            on rc.id = rr.referral_code_id
            where rc.account_id = $1
            offset {offset}
            limit {page_size}
        """
        return connection.fetch(query, account_id)

    @classmethod
    async def get_account_referrals_count(
        cls,
        connection: Connection,
        account_id: UUID,
    ) -> int:
        query = f"""select count(rr.account_id)
            from referral.codes rc
            left join referral.referrals rr
            on rc.id = rr.referral_code_id
            where rc.account_id = $1
        """
        val = connection.fetchval(query, account_id)
        if val is None:
            val = 0
        return val

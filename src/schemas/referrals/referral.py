from uuid import UUID

from pydantic import BaseModel


class ReferralSchema(BaseModel):
    account_id: UUID
    referral_code_id: UUID

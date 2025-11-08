from uuid import UUID

from msgspec import Struct


class ReferralDTO(Struct):
    account_id: UUID
    referral_code_id: UUID

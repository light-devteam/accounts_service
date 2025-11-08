from datetime import datetime
from uuid import UUID

from msgspec import Struct


class ReferralCodeDTO(Struct):
    id: UUID
    account_id: UUID
    code: str
    max_uses: int
    uses: int
    created_at: datetime
    is_available: bool = True
    expires_at: datetime | None = None
    target_telegram_id: int | None = None

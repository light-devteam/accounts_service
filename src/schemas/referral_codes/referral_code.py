from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, field_serializer


class ReferralCodeSchema(BaseModel):
    id: UUID
    account_id: UUID
    code: str
    max_uses: int
    uses: int
    created_at: datetime
    is_available: bool
    expires_at: datetime | None = None
    target_telegram_id: int | None = None

    @field_serializer(
        'created_at',
        'expires_at',
        when_used='json-unless-none',
    )
    def serialize_datetime(self, value: datetime) -> float:
        return value.timestamp()

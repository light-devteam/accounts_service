from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateReferralCodeSchema(BaseModel):
    account_id: UUID
    code: str = Field(min_length=1, max_length=32)  # max_length equals field varchar length in db
    max_uses: int = 0
    expires_at: Optional[datetime] = None
    target_telegram_id: Optional[int] = None

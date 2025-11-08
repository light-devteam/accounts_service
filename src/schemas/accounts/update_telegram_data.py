from typing import Optional

from pydantic import BaseModel, Field


class UpdateTelegramDataSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field('', min_length=0, max_length=64)
    username: Optional[str] = Field(None, min_length=3, max_length=32)

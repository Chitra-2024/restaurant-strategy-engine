from __future__ import annotations

from pydantic import BaseModel, Field


class DataFilterRequest(BaseModel):
    restaurant_name: str | None = Field(default=None)
    location: str | None = Field(default=None)
    days: int | None = Field(default=None, ge=1, le=365)

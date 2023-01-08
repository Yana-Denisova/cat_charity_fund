from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class GetUserDonations(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True

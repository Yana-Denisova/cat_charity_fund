from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class GetUserDonations(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationsDB(DonationBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
    user_id: int

    class Config:
        orm_mode = True

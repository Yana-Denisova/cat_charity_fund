from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator, Extra


class CharityProjectDB(BaseModel):
    name: str
    description: str
    full_amount: int
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt

    @validator('name')
    def name_cant_be_empty(cls, value: str):
        if not value:
            raise ValueError('Имя обязательно к заполнению!')
        return value

    @validator('description')
    def description_cant_be_empty(cls, value: str):
        if not value:
            raise ValueError('Описание обязательно к заполнению!')
        return value

    @validator('full_amount')
    def full_amount_cant_be_empty(cls, value: int):
        if not value:
            raise ValueError('Требуемая сумма обязательна к заполнению')
        return value

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

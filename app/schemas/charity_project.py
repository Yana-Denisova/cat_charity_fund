from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    @validator('name')
    def name_cant_be_empty(cls, value: str):
        if not value:
            raise ValueError('Имя обязательно к заполнению')
        return value

    @validator('description')
    def description_cant_be_empty(cls, value: str):
        if not value:
            raise ValueError('Описание обязательно к заполнению')
        return value

    @validator('full_amount')
    def full_amount_cant_be_empty(cls, value: int):
        if not value:
            raise ValueError('Требуемая сумма обязательна к заполнению')
        return value

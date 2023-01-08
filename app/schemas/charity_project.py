from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, validator


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[NonNegativeInt]

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value

    @validator('full_amount')
    def full_amount_cannot_be_zero(cls, value):
        if value == 0:
            raise ValueError('Всего лишь НОЛЬ для котиков? Серьёзно?')
        return value


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: NonNegativeInt

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

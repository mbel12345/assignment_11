'''
Pydantic schemas for validating calculation data.
Schemas define the shape of data coming in snd out of the API.
'''

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional
from uuid import UUID

class CalculationType(str, Enum):

    # Enumeration of valid calculation types

    ADDITION = 'addition'
    SUBTRACTION = 'subtraction'
    MULTIPLICATION = 'multiplication'
    DIVISION = 'division'

class CalculationBase(BaseModel):

    # Base schema for calculation data

    type: CalculationType = Field(
        ...,
        description='Type of calculation to perform',
        examples=['addition'],
    )

    a: float = Field(
        ...,
        description='First numeric input for the calculation',
        examples=[5, 3.5, -43, 0],
    )

    b: float = Field(
        ...,
        description='Second numeric input for the calculation',
        examples=[5, 3.5, -43, 0],
    )

    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, v):

        '''
        Validate and normalize the calculation type.
        Make sure it is a string and convert it to lowercase, for comparisons.
        '''

        allowed = {e.value for e in CalculationType}
        if not isinstance(v, str) or v.lower() not in allowed:
            raise ValueError(f'Type must be one of {', '.join(sorted(allowed))}')
        return v.lower()

    # validate_a is not needed as Pydantic does this automatically based on the Field Type

    @model_validator(mode='after')
    def validate_b(self) -> 'CalculationBase':

        # Validate b

        if self.type == CalculationType.DIVISION:
            if self.b == 0:
                raise ValueError('Cannot divide by zero.')
        return self

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'examples': [
                {'type': 'addition', 'a': 10.5, 'b': 4},
                {'type': 'subtraction', 'a': 10.5, 'b': 4},
                {'type': 'multiplication', 'a': 10.5, 'b': 4},
                {'type': 'division', 'a': 10.5, 'b': 4},
            ],
        },
    )

class CalculationCreate(CalculationBase):

    # Schema for creating a new Calculation

    user_id: UUID = Field(
        ...,
        description='UUID of the user who owns this calculation',
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {'type': 'addition', 'a': 10.5, 'b': 4},
                {'type': 'subtraction', 'a': 10.5, 'b': 4},
                {'type': 'multiplication', 'a': 10.5, 'b': 4},
                {'type': 'division', 'a': 10.5, 'b': 4},
            ],
        },
    )

class CalculationUpdate(BaseModel):

    '''
    Schema for updating a Calculation.
    Numeric validation is automatically done by Pydantic, so need for a validate method.
    '''

    a: Optional[float] = Field(
        None,
        description='First numeric input for the calculation',
        examples=[5, 3.5, -43, 0],
    )

    b: Optional[float] = Field(
        None,
        description='Second numeric input for the calculation',
        examples=[5, 3.5, -43, 0],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={'a': 10.5, 'b': 4},
    )

class CalculationRead(CalculationBase):

    # Schema for reading a Calculation from the database

    id: UUID = Field(
        ...,
        description='Unique UUID of the calculation',
        examples=["123e4567-e89b-12d3-a456-426614174999"],
    )

    user_id: UUID = Field(
        ...,
        description='UUID of the user who owns this calculation',
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    created_at: datetime = Field(
        ...,
        description='Time when the calculation was created',
    )

    updated_at: datetime = Field(
        ...,
        description='Time when the calculation was last updated',
    )

    result: float = Field(
        ...,
        description='Result of the calculation',
        examples=[19.5],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'id': '123e4567-e89b-12d3-a456-426614174999',
                'user_id': '123e4567-e89b-12d3-a456-426614174000',
                'type': 'addition',
                'a': 4.5,
                'b': 2.5,
                'result': 7,
                'created_at': '2026-01-01T00:00:00',
                'updated_at': '2026-01-01T00:00:00',
            },
        },
    )

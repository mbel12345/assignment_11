'''
Calculation Models with Polymorphic Inheritance.

Addition, Subtraction, Multiplication, and Division all inherit from a base Calculation Model.
'''

import uuid

from sqlalchemy import Column, Float, ForeignKey, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr, relationship, validates

from app.database import Base

class AbstractCalculation:

    # Abstract base class defining common attributes for all calculations

    @declared_attr
    def __tablename__(cls):

        # All calculation types share the 'calculations' table

        return 'calculations'

    @declared_attr
    def id(cls):

        # Unique ID for each calculation

        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False,
        )

    @declared_attr
    def user_id(cls):

        # Foreign key to the user who did the calculation

        return Column(
            UUID(as_uuid=True),
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False,
            index=True,
        )

    @declared_attr
    def type(cls):

        # Discriminator column for polymorphic inheritance.

        return Column(
            String(50),
            nullable=False,
            index=True,
        )

    '''
    Assignment 11 instructions say to use a and b (two inputs) rather than a variable number of inputs like in Module 11.
    '''

    @declared_attr
    def a(cls):

        # First number in the calcuation

        return Column(
            Float,
            nullable=False,
        )

    @declared_attr
    def b(cls):

        # Second number in the calcuation

        return Column(
            Float,
            nullable=False,
        )

    @validates('a', 'b')
    def validate_numbers(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f'{key} must be a number')
        return value

    @declared_attr
    def result(cls):

        # The result of the calculation

        return Column(
            Float,
            nullable=True,
        )

    @declared_attr
    def user(cls):

        # Relationship to the User model

        return relationship('User', back_populates='calculations')

    @classmethod
    def create(cls, calculation_type: str, user_id: uuid.UUID, a: float, b: float) -> 'Calculation':

        # Factory method to create the correct calculation subclass

        calculation_classes = {
            'addition': Addition,
            'subtraction': Subtraction,
            'multiplication': Multiplication,
            'division': Division,
        }
        calculation_class = calculation_classes.get(calculation_type.lower())
        if not calculation_class:
            raise ValueError(f'Unsupported calculation type: {calculation_type}')
        return calculation_class(user_id=user_id, a=a, b=b)

    def get_result(self) -> float:

        # Abstract method to compute the calculation result

        raise NotImplementedError(
            'Subclasses must implement get_result() method',
        )

    def __repr__(self):

        return f'<Calculation(type={self.type}, a={self.a}, b={self.b})>'

class Calculation(Base, AbstractCalculation):

    # Base Calculation model with polymorphic configuration

    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'calculation',
    }

class Addition(Calculation):

    # Addition calculation subclass

    __mapper_args__ = {'polymorphic_identity': 'addition'}

    def get_result(self) -> float:

        return self.a + self.b

class Subtraction(Calculation):

    # Subtraction calculation subclass

    __mapper_args__ = {'polymorphic_identity': 'subtraction'}

    def get_result(self) -> float:

        return self.a - self.b

class Multiplication(Calculation):

    # Multiplcation calculation subclass

    __mapper_args__ = {'polymorphic_identity': 'multiplication'}

    def get_result(self) -> float:

        return self.a * self.b

class Division(Calculation):

    # Division calculation subclass

    __mapper_args__ = {'polymorphic_identity': 'division'}

    def get_result(self) -> float:

        if self.b == 0:
            raise ValueError('Cannot divide by zero.')

        return self.a / self.b

import pytest

from datetime import datetime, timezone
from pydantic import ValidationError
from uuid import uuid4

from app.schemas.calculation import (
    CalculationBase,
    CalculationCreate,
    CalculationRead,
    CalculationType,
    CalculationUpdate,
)
def test_calculation_type_enum_values():

    # Test that CalculationType has the correct values

    assert CalculationType.ADDITION.value == 'addition'
    assert CalculationType.SUBTRACTION.value == 'subtraction'
    assert CalculationType.MULTIPLICATION.value == 'multiplication'
    assert CalculationType.DIVISION.value == 'division'

def test_calculation_base_valid_addition():

    # Test CalculationBase for a valid addition

    data = {
        'type': 'addition',
        'a': 2.5,
        'b': 5,
    }
    calc = CalculationBase(**data)
    assert calc.type == CalculationType.ADDITION
    assert calc.a == 2.5
    assert calc.b == 5

def test_calculation_base_valid_subtraction():

    # Test CalculationBase for a valid subtraction

    data = {
        'type': 'subtraction',
        'a': 2.5,
        'b': 5,
    }
    calc = CalculationBase(**data)
    assert calc.type == CalculationType.SUBTRACTION
    assert calc.a == 2.5
    assert calc.b == 5

def test_calculation_base_valid_multiplication():

    # Test CalculationBase for a valid multiplication

    data = {
        'type': 'multiplication',
        'a': 2.5,
        'b': 5,
    }
    calc = CalculationBase(**data)
    assert calc.type == CalculationType.MULTIPLICATION
    assert calc.a == 2.5
    assert calc.b == 5

def test_calculation_base_valid_division():

    # Test CalculationBase for a valid division

    data = {
        'type': 'division',
        'a': 2.5,
        'b': 5,
    }
    calc = CalculationBase(**data)
    assert calc.type == CalculationType.DIVISION
    assert calc.a == 2.5
    assert calc.b == 5

def test_calculation_base_case_insensitive_type():

    # Test that calculation type is case-insensitive

    for op in ['Addition', 'ADDITION', 'AdDiTiOn', 'addition']:
        data = {'type': op, 'a': 3, 'b': 5}
        calc = CalculationBase(**data)
        assert calc.type == CalculationType.ADDITION

def test_calculation_base_invalid_type():

    # Test that invalid calculation type raises ValidationError

    data = {
        'type': 'modulus',
        'a': 4,
        'b': 8,
    }
    with pytest.raises(ValidationError, match='Type must be one of'):
        CalculationBase(**data)

def test_calculation_base_invalid_a():

    # Test that non-numeric a raises ValidationError

    data = {
        'type': 'addition',
        'a': 'car',
        'b': 5,
    }
    with pytest.raises(ValidationError, match='Input should be a valid number'):
        CalculationBase(**data)

def test_calculation_base_invalid_b():

    # Test that non-numeric b raises ValidationError

    data = {
        'type': 'addition',
        'a': 9,
        'b': 'xyz',
    }
    with pytest.raises(ValidationError, match='Input should be a valid number'):
        CalculationBase(**data)

def test_calcuation_base_empty_a():

    # Test that empty a raises ValidationError

    data = {
        'type': 'multiplication',
        'a': None,
        'b': 0,
    }
    with pytest.raises(ValidationError, match='Input should be a valid number'):
        CalculationBase(**data)

def test_calcuation_base_empty_b():

    # Test that empty a raises ValidationError

    data = {
        'type': 'multiplication',
        'a': 0,
        'b': None,
    }
    with pytest.raises(ValidationError, match='Input should be a valid number'):
        CalculationBase(**data)

def test_calculation_base_division_by_zero():

    # Test that division by zero is caught by schema validation

    data = {
        'type': 'division',
        'a': 4,
        'b': 0,
    }

    with pytest.raises(ValidationError, match='Cannot divide by zero.'):
        CalculationBase(**data)

def test_calcluation_base_division_by_zero_numerator_ok():

    # Test that division by zero works when numerator (a) is zero

    data = {
        'type': 'division',
        'a': 0,
        'b': 4,
    }

    calc = CalculationBase(**data)
    assert calc.a == 0
    assert calc.b == 4

def test_calculation_create_valid():

    # Test CalculationCreate with valid data

    user_id = uuid4()
    data = {
        'type': 'multiplication',
        'a': 5,
        'b': 10,
        'user_id': str(user_id),
    }
    calc = CalculationCreate(**data)
    assert calc.type == CalculationType.MULTIPLICATION
    assert calc.a == 5
    assert calc.b == 10
    assert calc.user_id == user_id

def test_calculation_create_missing_type():

    # Test that CalculationCreate requires type

    data = {
        # 'type': 'addition', # Missing
        'a': 3,
        'b': 4,
        'user_id': str(uuid4()),
    }
    with pytest.raises(ValidationError, match=r'1 validation error for CalculationCreate\s+type'):
        CalculationCreate(**data)

def test_calculation_create_missing_a():

    # Test that CalculationCreate requires a

    data = {
        'type': 'addition',
        # 'a': 3, # Missing
        'b': 4,
        'user_id': str(uuid4()),
    }
    with pytest.raises(ValidationError, match=r'1 validation error for CalculationCreate\s+a'):
        CalculationCreate(**data)

def test_calculation_create_missing_b():

    # Test that CalculationCreate requires b

    data = {
        'type': 'addition',
        'a': 3,
        # 'b': 4, # Missing
        'user_id': str(uuid4()),
    }
    with pytest.raises(ValidationError, match=r'1 validation error for CalculationCreate\s+b'):
        CalculationCreate(**data)

def test_calculation_create_missing_user_id():

    # Test that CalculationCreate requires user_id

    data = {
        'type': 'addition',
        'a': 3,
        'b': 4,
        # 'user_id': str(uuid4()), # Missing
    }
    with pytest.raises(ValidationError, match=r'1 validation error for CalculationCreate\s+user_id'):
        CalculationCreate(**data)

def test_calculation_create_invalid_user_id():

    # Test that invalid UUID format raises ValidationError

    data = {
        'type': 'subtraction',
        'a': 5,
        'b': 10,
        'user_id': 'invalid_uuid',
    }

    with pytest.raises(ValidationError, match=r'1 validation error for CalculationCreate\s+user_id'):
        CalculationCreate(**data)

def test_calculation_update_valid():

    # Test CalculationUpdate with valid data

    data = {
        'a': 6,
        'b': 8,
    }
    calc = CalculationUpdate(**data)
    assert calc.a == 6
    assert calc.b == 8

def test_calculation_update_a_optional():

    # Test that CalculationUpdate can have empty a

    data = {'b': 4}
    calc = CalculationUpdate(**data)
    assert calc.a is None
    assert calc.b == 4

def test_calculation_update_b_optional():

    # Test that CalculationUpdate can have empty b

    data = {'a': 4}
    calc = CalculationUpdate(**data)
    assert calc.a == 4
    assert calc.b is None

def test_calculation_read_valid():

    # Test CalculationResonse with all required fields

    data = {
        'id': str(uuid4()),
        'user_id': str(uuid4()),
        'type': 'addition',
        'a': 5,
        'b': 8,
        'result': 13,
        'created_at': datetime.now(timezone.utc),
        'updated_at': datetime.now(timezone.utc),
    }
    calc = CalculationRead(**data)
    assert calc.result == 13
    assert calc.type == CalculationType.ADDITION

def test_calculation_read_missing_result():

    # Test CalculationResonse with all required fields

    data = {
        'id': str(uuid4()),
        'user_id': str(uuid4()),
        'type': 'addition',
        'a': 5,
        'b': 8,
        # 'result': 13, # Missing
        'created_at': datetime.now(timezone.utc),
        'updated_at': datetime.now(timezone.utc),
    }

    with pytest.raises(ValidationError, match=r'1 validation error for CalculationRead\s+result'):
        CalculationRead(**data)

def test_multiple_calculations_with_different_types():

    # Test that schemas correctly validate multiple calculations of different types

    user_id = uuid4()

    calcs_data = [
        {'type': 'addition', 'a': 2, 'b': 4, 'user_id': str(user_id)},
        {'type': 'subtraction', 'a': 2, 'b': 4, 'user_id': str(user_id)},
        {'type': 'multiplication', 'a': 2, 'b': 4, 'user_id': str(user_id)},
        {'type': 'division', 'a': 2, 'b': 4, 'user_id': str(user_id)},
    ]

    calcs = [CalculationCreate(**data) for data in calcs_data]

    assert len(calcs) == 4
    assert calcs[0].type == CalculationType.ADDITION
    assert calcs[0].type == CalculationType.ADDITION
    assert calcs[0].type == CalculationType.ADDITION
    assert calcs[0].type == CalculationType.ADDITION

def test_schema_with_large_numbers():

    # Test that schemas handle large numbers correctly

    data = {
        'type': 'multiplication',
        'a': 1e10,
        'b': 1e20,
    }
    calc = CalculationBase(**data)
    assert isinstance(calc.a, float)
    assert isinstance(calc.b, float)

def test_schema_with_negative_numbers():

    # Test that schemas handle negative numbers correctly

    data = {
        'type': 'addition',
        'a': 5,
        'b': -9,
    }
    calc = CalculationBase(**data)
    assert isinstance(calc.a, float)
    assert isinstance(calc.b, float)

def test_schema_with_int_and_float():

    # Test that schemas handle ints and floats being used together

    data = {
        'type': 'addition',
        'a': 5,
        'b': -9.8,
    }
    calc = CalculationBase(**data)
    assert isinstance(calc.a, float)
    assert isinstance(calc.b, float)

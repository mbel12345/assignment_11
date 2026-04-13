import pytest
import uuid

from app.models.calculation import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
)

'''
This class is used for testing that the arithmetic operations work on various input combinations with varied numeric types.
'''

def dummy_user_id():

    # Generate a random UUID for testing purposes

    return uuid.uuid4()

@pytest.mark.parametrize(
    'a, b, expected',
    [
        (2, 3, 5),           # Test with two positive integers
        (-2, -3, -5),        # Test with two negative integers
        (2.5, 7.5, 10),     # Test with two positive floats
        (-2.5, 4, 1.5),    # Test with a negative float and a positive float
        (0, 0, 0),           # Test with zeros
    ],
    ids=[
        'add_two_positive_integers',
        'add_two_negative_integers',
        'add_two_positive_floats',
        'add_negative_and_positive_float',
        'add_zeros',
    ]
)
def test_add(a: float, b: float, expected: float) -> None:

    # Test the add function

    operation = Addition(user_id=dummy_user_id(), a=a, b=b)
    actual = operation.get_result()
    assert actual == expected, f'Expected {expected}, got {actual}'

@pytest.mark.parametrize(
    'a, b, expected',
    [
        (2, 3, -1),           # Test with two positive integers
        (-2, -3, 1),        # Test with two negative integers
        (2.5, 7.5, -5),     # Test with two positive floats
        (-2.5, 4, -6.5),    # Test with a negative float and a positive float
        (0, 0, 0),           # Test with zeros
    ],
    ids=[
        'subtract_two_positive_integers',
        'subtract_two_negative_integers',
        'subtract_two_positive_floats',
        'subtract_negative_and_positive_float',
        'subtract_zeros',
    ]
)
def test_subtract(a: float, b: float, expected: float) -> None:

    # Test the subtract function

    operation = Subtraction(user_id=dummy_user_id(), a=a, b=b)
    actual = operation.get_result()
    assert actual == expected, f'Expected {expected}, got {actual}'

@pytest.mark.parametrize(
    'a, b, expected',
    [
        (2, 4, 8),           # Test with two positive integers
        (-2, -5, 10),        # Test with two negative integers
        (2.5, 4, 10),     # Test with two positive floats
        (-2.5, 4, -10),    # Test with a negative float and a positive float
        (0, 0, 0),           # Test with zeros
    ],
    ids=[
        'divide_two_positive_integers',
        'divide_two_negative_integers',
        'divide_two_positive_floats',
        'divide_negative_and_positive_float',
        'divide_zeros',
    ]
)
def test_multiply(a: float, b: float, expected: float) -> None:

    # Test the multiply function

    operation = Multiplication(user_id=dummy_user_id(), a=a, b=b)
    actual = operation.get_result()
    assert actual == expected, f'Expected {expected}, got {actual}'

@pytest.mark.parametrize(
    'a, b, expected',
    [
        (2, 4, 0.5),           # Test with two positive integers
        (-2, -5, 0.4),        # Test with two negative integers
        (2.5, 4, 0.625),     # Test with two positive floats
        (-2.5, 4, -0.625),    # Test with a negative float and a positive float
        (0, 8, 0),           # Test with zeros
    ],
    ids=[
        'multiply_two_positive_integers',
        'multiply_two_negative_integers',
        'multiply_two_positive_floats',
        'multiply_negative_and_positive_float',
        'multiply_zeros',
    ]
)
def test_divide(a: float, b: float, expected: float) -> None:

    # Test the divide function

    operation = Division(user_id=dummy_user_id(), a=a, b=b)
    actual = operation.get_result()
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_divide_by_zero() -> None:

    # Test that divide raises an error on division by zero
    with pytest.raises(ValueError, match='Cannot divide by zero.'):
        Division(user_id=dummy_user_id(), a=5, b=0).get_result()

import pytest
import re
import uuid

from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
)

def dummy_user_id():

    # Generate a random UUID for testing purposes

    return uuid.uuid4()

def test_addition_get_result():

    # Test that Addition.get_result returns the correct sum.

    addition = Addition(user_id=dummy_user_id(), a=6, b=8)
    actual = addition.get_result()
    expected = 14
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_subtraction_get_result():

    # Test that Subtraction.get_result returns the correct difference.

    subtraction = Subtraction(user_id=dummy_user_id(), a=6, b=8)
    actual = subtraction.get_result()
    expected = -2
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_multiplication_get_result():

    # Test that Multiplication.get_result returns the correct product.

    multiplication = Multiplication(user_id=dummy_user_id(), a=6, b=8)
    actual = multiplication.get_result()
    expected = 48
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_division_get_result():

    # Test that Division.get_result returns the correct quotient.

    addition = Division(user_id=dummy_user_id(), a=6, b=8)
    actual = addition.get_result()
    expected = 0.75
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_division_by_zero():

    # Test that Divison.get_result raises ValueError for zero division

    division = Division(user_id=dummy_user_id(), a=6, b=0)
    with pytest.raises(ValueError, match='Cannot divide by zero.'):
        division.get_result()

def test_calculation_factory_addition():

    # Test Calculation.create factory method for addition

    calc = Calculation.create(
        calculation_type='addition',
        user_id=dummy_user_id(),
        a=8,
        b=10,
    )
    assert isinstance(calc, Addition), 'Factory did not return an Addition instance.'
    assert isinstance(calc, Calculation), 'Addition should also be an instance of Calculation.'
    actual = calc.get_result()
    expected = 18
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_calculation_factory_subtraction():

    # Test Calculation.create factory method for subtraction

    calc = Calculation.create(
        calculation_type='subtraction',
        user_id=dummy_user_id(),
        a=8,
        b=10,
    )
    assert isinstance(calc, Subtraction), 'Factory did not return a Subtraction instance.'
    assert isinstance(calc, Calculation), 'Subtraction should also be an instance of Calculation.'
    actual = calc.get_result()
    expected = -2
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_calculation_factory_multiplication():

    # Test Calculation.create factory method for multiplication

    calc = Calculation.create(
        calculation_type='multiplication',
        user_id=dummy_user_id(),
        a=8,
        b=10,
    )
    assert isinstance(calc, Multiplication), 'Factory did not return a Multiplication instance.'
    assert isinstance(calc, Calculation), 'Multiplication should also be an instance of Calculation.'
    actual = calc.get_result()
    expected = 80
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_calculation_factory_division():

    # Test Calculation.create factory method for division

    calc = Calculation.create(
        calculation_type='division',
        user_id=dummy_user_id(),
        a=8,
        b=10,
    )
    assert isinstance(calc, Division), 'Factory did not return a Division instance.'
    assert isinstance(calc, Calculation), 'Division should also be an instance of Calculation.'
    actual = calc.get_result()
    expected = 0.8
    assert actual == expected, f'Expected {expected}, got {actual}'

def test_calculation_factory_invalid_type():

    # Test that Calculation.create raises a ValueError for unsupported types

    with pytest.raises(ValueError, match='Unsupported calculation type'):
        Calculation.create(
            calculation_type='modulus',
            user_id=dummy_user_id(),
            a=10,
            b=3,
        )

def test_calculation_factory_case_insensitive():

    # Test that the factory is case-insensitive

    for calc_type in ['addition', 'Addition', 'ADDITION', 'AdDiTiOn']:
        calc = Calculation.create(
            calculation_type=calc_type,
            user_id=dummy_user_id(),
            a=8,
            b=10,
        )
        assert isinstance(calc, Addition), f'History failed for case: {calc_type}'
        actual = calc.get_result()
        expected = 18
        assert actual == expected, f'Expected {expected}, got {actual}'

def test_invalid_inputs_for_addition():

    # Test that invalid inputs for addition raises error

    with pytest.raises(ValueError, match='a must be a number'):
        Addition(user_id=dummy_user_id(), a='car', b=6)

def test_invalid_inputs_for_subtraction():

    # Test that invalid inputs for subtraction raises error

    with pytest.raises(ValueError, match='a must be a number'):
        Subtraction(user_id=dummy_user_id(), a='car', b=6)

def test_invalid_inputs_for_multiplication():

    # Test that invalid inputs for multiplication raises error

    with pytest.raises(ValueError, match='a must be a number'):
        Multiplication(user_id=dummy_user_id(), a='car', b=6)

def test_invalid_inputs_for_division():

    # Test that invalid inputs for division raises error

    with pytest.raises(ValueError, match='a must be a number'):
        Division(user_id=dummy_user_id(), a='car', b=6)

def test_polymorphic_list_of_calculations():

    # Test that different calculation types can be stored in the same list

    user_id = dummy_user_id()

    calculations =[
        Calculation.create('addition', user_id, 4, 5),
        Calculation.create('subtraction', user_id, 4, 5),
        Calculation.create('multiplication', user_id, 4, 5),
        Calculation.create('division', user_id, 4, 5),
    ]

    assert isinstance(calculations[0], Addition)
    assert isinstance(calculations[1], Subtraction)
    assert isinstance(calculations[2], Multiplication)
    assert isinstance(calculations[3], Division)

    result = [calc.get_result() for calc in calculations]
    assert result == [9, -1, 20, 0.8]

def test_polymorphic_method_calling():

    user_id = dummy_user_id()

    calc_types = ['addition', 'subtraction', 'multiplication', 'division']
    expecteds = [7, -1, 12, 0.75]

    for calc_type, expected in zip(calc_types, expecteds):
        calc = Calculation.create(calc_type, user_id, 3, 4)
        actual = calc.get_result()
        assert actual == expected, f'{calc_type} failed: Expected {expected}, got {actual}'

def test_unimplented_get_result():

    # Test that a Calculation sub-class throws an NotImplementedError exception if get_result() is called when it is not defined in the subclass

    class Modulus(Calculation):

        __mapper_args__ = {
            'polymorphic_identity': 'modulus',
        }

    m = Modulus(user_id=dummy_user_id(), type='modulus', a=0, b=0)
    with pytest.raises(NotImplementedError, match=re.escape('Subclasses must implement get_result() method')):
        m.get_result()

def test_repr():

    # Test str representation of a Calculation

    calc = Calculation.create('addition', dummy_user_id(), 3, 4)
    actual = str(calc)
    expected = '<Calculation(type=addition, a=3, b=4)>'

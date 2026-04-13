from datetime import datetime, timezone
from sqlalchemy import select

from app.models.calculation import Calculation
from app.models.user import User

def add_test_user(db_session):

    # Helper method to create a dummy user

    data = {
        'username': 'john.a',
        'email': 'john.a@gmail.com',
    }
    user = User(**data)

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user.id

def test_add_addition_calculation_to_db(db_session):

    # Test adding an addition to DB, and do a select query to verify

    user_id = add_test_user(db_session)

    data = {
        'calculation_type': 'addition',
        'a': 5,
        'b': 10,
        'user_id': user_id,
    }
    calc = Calculation.create(**data)
    calc.set_result()
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    stmt = (
        select(
            Calculation.user_id.label('user_id'),
            Calculation.type.label('type'),
            Calculation.a.label('a'),
            Calculation.b.label('b'),
            Calculation.result.label('result'),
            Calculation.created_at.label('created_at'),
            Calculation.created_at.label('updated_at'),
        )
    )
    actual = db_session.execute(stmt).all()
    actual = dict(actual[0]._mapping)

    now = datetime.now(timezone.utc)
    created_at = actual['created_at'].replace(tzinfo=timezone.utc)
    assert abs((now - created_at).total_seconds()) < 5
    updated_at = actual['updated_at'].replace(tzinfo=timezone.utc)
    assert abs((now - updated_at).total_seconds()) < 5

    expected = {
        'type': 'addition',
        'a': 5.0,
        'b': 10.0,
        'result': 15.0,
        'user_id': user_id,
    }
    del(actual['created_at'])
    del(actual['updated_at'])
    assert actual == expected

def test_add_subtraction_calculation_to_db(db_session):

    # Test adding a subtraction to DB, and do a select query to verify

    user_id = add_test_user(db_session)

    data = {
        'calculation_type': 'subtraction',
        'a': 5,
        'b': 10,
        'user_id': user_id,
    }
    calc = Calculation.create(**data)
    calc.set_result()
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    stmt = (
        select(
            Calculation.user_id.label('user_id'),
            Calculation.type.label('type'),
            Calculation.a.label('a'),
            Calculation.b.label('b'),
            Calculation.result.label('result'),
            Calculation.created_at.label('created_at'),
            Calculation.created_at.label('updated_at'),
        )
    )
    actual = db_session.execute(stmt).all()
    actual = dict(actual[0]._mapping)

    now = datetime.now(timezone.utc)
    created_at = actual['created_at'].replace(tzinfo=timezone.utc)
    assert abs((now - created_at).total_seconds()) < 5
    updated_at = actual['updated_at'].replace(tzinfo=timezone.utc)
    assert abs((now - updated_at).total_seconds()) < 5

    expected = {
        'type': 'subtraction',
        'a': 5.0,
        'b': 10.0,
        'result': -5.0,
        'user_id': user_id,
    }
    del(actual['created_at'])
    del(actual['updated_at'])
    assert actual == expected

def test_add_multiplication_calculation_to_db(db_session):

    # Test adding a multiplication to DB, and do a select query to verify

    user_id = add_test_user(db_session)

    data = {
        'calculation_type': 'multiplication',
        'a': 5,
        'b': 10,
        'user_id': user_id,
    }
    calc = Calculation.create(**data)
    calc.set_result()
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    stmt = (
        select(
            Calculation.user_id.label('user_id'),
            Calculation.type.label('type'),
            Calculation.a.label('a'),
            Calculation.b.label('b'),
            Calculation.result.label('result'),
            Calculation.created_at.label('created_at'),
            Calculation.created_at.label('updated_at'),
        )
    )
    actual = db_session.execute(stmt).all()
    actual = dict(actual[0]._mapping)

    now = datetime.now(timezone.utc)
    created_at = actual['created_at'].replace(tzinfo=timezone.utc)
    assert abs((now - created_at).total_seconds()) < 5
    updated_at = actual['updated_at'].replace(tzinfo=timezone.utc)
    assert abs((now - updated_at).total_seconds()) < 5

    expected = {
        'type': 'multiplication',
        'a': 5.0,
        'b': 10.0,
        'result': 50.0,
        'user_id': user_id,
    }
    del(actual['created_at'])
    del(actual['updated_at'])
    assert actual == expected


def test_add_division_calculation_to_db(db_session):

    # Test adding a division to DB, and do a select query to verify

    user_id = add_test_user(db_session)

    data = {
        'calculation_type': 'division',
        'a': 5,
        'b': 10,
        'user_id': user_id,
    }
    calc = Calculation.create(**data)
    calc.set_result()
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    stmt = (
        select(
            Calculation.user_id.label('user_id'),
            Calculation.type.label('type'),
            Calculation.a.label('a'),
            Calculation.b.label('b'),
            Calculation.result.label('result'),
            Calculation.created_at.label('created_at'),
            Calculation.created_at.label('updated_at'),
        )
    )
    actual = db_session.execute(stmt).all()
    actual = dict(actual[0]._mapping)

    now = datetime.now(timezone.utc)
    created_at = actual['created_at'].replace(tzinfo=timezone.utc)
    assert abs((now - created_at).total_seconds()) < 5
    updated_at = actual['updated_at'].replace(tzinfo=timezone.utc)
    assert abs((now - updated_at).total_seconds()) < 5

    expected = {
        'type': 'division',
        'a': 5.0,
        'b': 10.0,
        'result': 0.5,
        'user_id': user_id,
    }
    del(actual['created_at'])
    del(actual['updated_at'])
    assert actual == expected

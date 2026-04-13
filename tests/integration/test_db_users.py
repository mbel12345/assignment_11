from datetime import datetime, timezone
from sqlalchemy import select

from app.models.user import User

def test_add_user_to_db(db_session):

    # Test adding a user to DB, and do a select query to verify

    data = {
        'username': 'john.a',
        'email': 'john.a@gmail.com',
    }
    user = User(**data)

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    stmt = (
        select(
            User.username.label('username'),
            User.email.label('email'),
            User.created_at.label('created_at'),
            User.updated_at.label('updated_at'),
        )
    )
    actual = db_session.execute(stmt).all()
    actual = dict(actual[0]._mapping)

    now = datetime.now(timezone.utc)
    created_at = actual['created_at'].replace(tzinfo=timezone.utc)
    assert abs((now - created_at).total_seconds()) < 5
    updated_at = actual['updated_at'].replace(tzinfo=timezone.utc)
    assert abs((now - updated_at).total_seconds()) < 5

    del(actual['created_at'])
    del(actual['updated_at'])
    assert actual == data

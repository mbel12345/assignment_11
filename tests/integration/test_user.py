from app.models.user import User

def test_create_user_and_repr():

    user = User(username='user_1', email='user_1@gmail.com')
    actual = str(user)
    expected = f'<User(username=user_1, email=user_1@gmail.com)>'
    assert actual == expected, f'Expected {expected}, got {actual}'

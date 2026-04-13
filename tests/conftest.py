import pytest

from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.database import get_engine

@pytest.fixture
def db_session():

    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        yield session
    finally:
        session.close()

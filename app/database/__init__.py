from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine(database_url: str = SQLALCHEMY_DATABASE_URL):

    '''
    Factory function to create a new SQLAlchemy engine.
    This is useful for testing or when you need to create engines with different configurations.
    '''

    return create_engine(database_url)

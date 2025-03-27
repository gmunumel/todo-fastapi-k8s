import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base

# Setup in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)  # Create tables
    my_db = TestingSessionLocal()
    try:
        yield my_db
    finally:
        my_db.close()
        Base.metadata.drop_all(bind=engine)  # Drop tables after test

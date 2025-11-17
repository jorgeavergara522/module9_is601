"""
Pytest configuration for integration tests.
Provides database fixtures for testing.
"""

import pytest
from app.database import Base, engine


@pytest.fixture(scope="function")
def db_setup():
    """
    Create all database tables before each test.
    Drop all tables after each test to ensure clean state.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)

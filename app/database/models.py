"""
SQLAlchemy User model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model for storing user accounts.
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Username - must be unique
    username = Column(String(50), unique=True, nullable=False, index=True)
    
    # Email - must be unique
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # Password hash - NEVER store plain text!
    password_hash = Column(String(255), nullable=False)
    
    # Timestamp - automatically set when user is created
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

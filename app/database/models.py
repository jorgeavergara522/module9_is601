"""
SQLAlchemy User model.
"""

from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
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
	
    # Relationship to calculations
    calculations = relationship("Calculation", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Calculation(Base):
    """Base Calculation model with polymorphic inheritance."""
    __tablename__ = "calculations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    inputs = Column(JSON, nullable=False)
    result = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    user = relationship("User", back_populates="calculations")
    
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "calculation"}
    
    @classmethod
    def create(cls, calculation_type: str, user_id: int, inputs: List[float]) -> "Calculation":
        """Factory method to create appropriate calculation subclass."""
        calculation_classes = {
            'addition': Addition, 'subtraction': Subtraction,
            'multiplication': Multiplication, 'division': Division,
        }
        calculation_class = calculation_classes.get(calculation_type.lower())
        if not calculation_class:
            raise ValueError(f"Unsupported calculation type: {calculation_type}")
        return calculation_class(user_id=user_id, inputs=inputs)
    
    def get_result(self) -> float:
        """Abstract method - subclasses must implement."""
        raise NotImplementedError("Subclasses must implement get_result() method")
    
    def __repr__(self):
        return f"<Calculation(id={self.id}, type={self.type})>"


class Addition(Calculation):
    """Addition: sums all numbers."""
    __mapper_args__ = {"polymorphic_identity": "addition"}
    
    def get_result(self) -> float:
        if not isinstance(self.inputs, list) or len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        return sum(self.inputs)


class Subtraction(Calculation):
    """Subtraction: first - second - third..."""
    __mapper_args__ = {"polymorphic_identity": "subtraction"}
    
    def get_result(self) -> float:
        if not isinstance(self.inputs, list) or len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        result = self.inputs[0]
        for value in self.inputs[1:]:
            result -= value
        return result


class Multiplication(Calculation):
    """Multiplication: multiplies all numbers."""
    __mapper_args__ = {"polymorphic_identity": "multiplication"}
    
    def get_result(self) -> float:
        if not isinstance(self.inputs, list) or len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        result = 1
        for value in self.inputs:
            result *= value
        return result


class Division(Calculation):
    """Division: first / second / third..."""
    __mapper_args__ = {"polymorphic_identity": "division"}
    
    def get_result(self) -> float:
        if not isinstance(self.inputs, list) or len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        result = self.inputs[0]
        for value in self.inputs[1:]:
            if value == 0:
                raise ValueError("Cannot divide by zero.")
            result /= value
        return result

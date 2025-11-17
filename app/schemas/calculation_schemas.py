"""
Calculation Pydantic Schemas

These schemas validate calculation data at the API boundary.
Pydantic provides automatic validation, serialization, and documentation.
"""

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator
from typing import List, Optional
from datetime import datetime

class CalculationType(str, Enum):
    """
    Enumeration of valid calculation types.
    
    Using an Enum provides type safety and auto-completion.
    """
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"

class CalculationBase(BaseModel):
    """Base schema for calculation data."""
    type: CalculationType = Field(..., description="Type of calculation to perform")
    inputs: List[float] = Field(..., description="List of numbers", min_length=2)

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v):
        """Validate and normalize type to lowercase."""
        allowed = {e.value for e in CalculationType}
        if not isinstance(v, str) or v.lower() not in allowed:
            raise ValueError(f"Type must be one of: {', '.join(sorted(allowed))}")
        return v.lower()

    @field_validator("inputs", mode="before")
    @classmethod
    def check_inputs_is_list(cls, v):
        """Validate that inputs is a list."""
        if not isinstance(v, list):
            raise ValueError("Input should be a valid list")
        return v

    @model_validator(mode='after')
    def validate_inputs(self) -> "CalculationBase":
        """Validate inputs based on calculation type."""
        if len(self.inputs) < 2:
            raise ValueError("At least two numbers are required")
        if self.type == CalculationType.DIVISION:
            if any(x == 0 for x in self.inputs[1:]):
                raise ValueError("Cannot divide by zero")
        return self

    model_config = ConfigDict(from_attributes=True)


class CalculationCreate(CalculationBase):
    """Schema for creating a new Calculation."""
    user_id: int = Field(..., description="ID of the user who owns this calculation")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "addition",
                "inputs": [10.5, 3, 2],
                "user_id": 1
            }
        }
    )


class CalculationUpdate(BaseModel):
    """Schema for updating an existing Calculation."""
    inputs: Optional[List[float]] = Field(None, description="Updated list of numbers", min_length=2)

    @model_validator(mode='after')
    def validate_inputs(self) -> "CalculationUpdate":
        """Validate inputs if they are being updated."""
        if self.inputs is not None and len(self.inputs) < 2:
            raise ValueError("At least two numbers are required")
        return self

    model_config = ConfigDict(from_attributes=True)

class CalculationResponse(CalculationBase):
    """Schema for reading a Calculation from the database."""
    id: int = Field(..., description="Unique ID of the calculation")
    user_id: int = Field(..., description="ID of the user who owns this")
    result: float = Field(..., description="Result of the calculation")
    created_at: datetime = Field(..., description="When created")
    updated_at: datetime = Field(..., description="When last updated")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "type": "addition",
                "inputs": [10.5, 3, 2],
                "result": 15.5,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }
    )



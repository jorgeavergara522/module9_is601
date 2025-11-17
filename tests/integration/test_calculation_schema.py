"""
Integration Tests for Calculation Pydantic Schemas
Tests both valid and invalid data validation.
"""

import pytest
from pydantic import ValidationError
from app.schemas.calculation_schemas import (
    CalculationType, CalculationBase, CalculationCreate,
    CalculationUpdate, CalculationResponse
)
from datetime import datetime


def test_calculation_type_enum_values():
    """Test CalculationType enum values."""
    assert CalculationType.ADDITION.value == "addition"
    assert CalculationType.SUBTRACTION.value == "subtraction"
    assert CalculationType.MULTIPLICATION.value == "multiplication"
    assert CalculationType.DIVISION.value == "division"


def test_calculation_base_valid():
    """Test CalculationBase with valid data."""
    data = {"type": "addition", "inputs": [10.5, 3, 2]}
    calc = CalculationBase(**data)
    assert calc.type == CalculationType.ADDITION
    assert calc.inputs == [10.5, 3, 2]


def test_calculation_base_case_insensitive():
    """Test type is case-insensitive."""
    for variant in ["Addition", "ADDITION", "addition"]:
        data = {"type": variant, "inputs": [1, 2]}
        calc = CalculationBase(**data)
        assert calc.type == CalculationType.ADDITION


def test_calculation_base_invalid_type():
    """Test invalid type raises error."""
    data = {"type": "modulus", "inputs": [10, 3]}
    with pytest.raises(ValidationError):
        CalculationBase(**data)


def test_calculation_base_inputs_not_list():
    """Test non-list inputs raise error."""
    data = {"type": "addition", "inputs": "not a list"}
    with pytest.raises(ValidationError):
        CalculationBase(**data)


def test_calculation_base_insufficient_inputs():
    """Test fewer than 2 inputs raises error."""
    data = {"type": "addition", "inputs": [5]}
    with pytest.raises(ValidationError):
        CalculationBase(**data)


def test_calculation_base_division_by_zero():
    """Test division by zero is rejected."""
    data = {"type": "division", "inputs": [100, 0]}
    with pytest.raises(ValidationError):
        CalculationBase(**data)


def test_calculation_create_valid():
    """Test CalculationCreate with valid data."""
    data = {"type": "multiplication", "inputs": [2, 3, 4], "user_id": 1}
    calc = CalculationCreate(**data)
    assert calc.type == CalculationType.MULTIPLICATION
    assert calc.user_id == 1


def test_calculation_create_missing_user_id():
    """Test CalculationCreate requires user_id."""
    data = {"type": "addition", "inputs": [1, 2]}
    with pytest.raises(ValidationError):
        CalculationCreate(**data)


def test_calculation_update_valid():
    """Test CalculationUpdate with valid data."""
    data = {"inputs": [42, 7]}
    calc = CalculationUpdate(**data)
    assert calc.inputs == [42, 7]


def test_calculation_response_valid():
    """Test CalculationResponse with all fields."""
    data = {
        "id": 1, "user_id": 1, "type": "addition",
        "inputs": [10, 5], "result": 15.0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    calc = CalculationResponse(**data)
    assert calc.result == 15.0


def test_schema_with_negative_numbers():
    """Test schemas accept negative numbers."""
    data = {"type": "addition", "inputs": [-5, -10, 3.5]}
    calc = CalculationBase(**data)
    assert calc.inputs == [-5, -10, 3.5]

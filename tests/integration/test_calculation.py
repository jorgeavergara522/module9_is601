"""
Integration Tests for Polymorphic Calculation Models

These tests verify the polymorphic behavior of the Calculation model hierarchy.
Tests the Factory Pattern and type-specific behavior.
"""

import pytest
from app.database.models import Calculation, Addition, Subtraction, Multiplication, Division

def test_addition_get_result():
    """Test that Addition correctly sums all numbers."""
    addition = Addition(user_id=1, inputs=[10, 5, 3.5])
    result = addition.get_result()
    assert result == 18.5, f"Expected 18.5, got {result}"


def test_subtraction_get_result():
    """Test that Subtraction correctly subtracts sequentially."""
    subtraction = Subtraction(user_id=1, inputs=[20, 5, 3])
    result = subtraction.get_result()
    assert result == 12, f"Expected 12, got {result}"


def test_multiplication_get_result():
    """Test that Multiplication correctly multiplies all numbers."""
    multiplication = Multiplication(user_id=1, inputs=[2, 3, 4])
    result = multiplication.get_result()
    assert result == 24, f"Expected 24, got {result}"


def test_division_get_result():
    """Test that Division correctly divides sequentially."""
    division = Division(user_id=1, inputs=[100, 2, 5])
    result = division.get_result()
    assert result == 10, f"Expected 10, got {result}"


def test_division_by_zero():
    """Test that Division raises ValueError when dividing by zero."""
    division = Division(user_id=1, inputs=[50, 0, 5])
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        division.get_result()


def test_calculation_factory_addition():
    """Test the Calculation.create factory method for addition."""
    calc = Calculation.create('addition', user_id=1, inputs=[1, 2, 3])
    assert isinstance(calc, Addition), "Factory did not return Addition instance"
    assert isinstance(calc, Calculation), "Addition should be instance of Calculation"
    assert calc.get_result() == 6, "Incorrect addition result"


def test_calculation_factory_subtraction():
    """Test the Calculation.create factory method for subtraction."""
    calc = Calculation.create('subtraction', user_id=1, inputs=[10, 4])
    assert isinstance(calc, Subtraction), "Factory did not return Subtraction instance"
    assert calc.get_result() == 6, "Incorrect subtraction result"


def test_calculation_factory_multiplication():
    """Test the Calculation.create factory method for multiplication."""
    calc = Calculation.create('multiplication', user_id=1, inputs=[3, 4, 2])
    assert isinstance(calc, Multiplication), "Factory did not return Multiplication instance"
    assert calc.get_result() == 24, "Incorrect multiplication result"


def test_calculation_factory_division():
    """Test the Calculation.create factory method for division."""
    calc = Calculation.create('division', user_id=1, inputs=[100, 2, 5])
    assert isinstance(calc, Division), "Factory did not return Division instance"
    assert calc.get_result() == 10, "Incorrect division result"


def test_calculation_factory_invalid_type():
    """Test that factory raises ValueError for unsupported types."""
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create('modulus', user_id=1, inputs=[10, 3])


def test_calculation_factory_case_insensitive():
    """Test that the factory is case-insensitive."""
    for calc_type in ['addition', 'Addition', 'ADDITION']:
        calc = Calculation.create(calc_type, user_id=1, inputs=[5, 3])
        assert isinstance(calc, Addition), f"Factory failed for case: {calc_type}"
        assert calc.get_result() == 8

def test_invalid_inputs_for_addition():
    """Test that non-list inputs raise ValueError."""
    addition = Addition(user_id=1, inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list"):
        addition.get_result()


def test_insufficient_inputs():
    """Test that fewer than 2 inputs raises ValueError."""
    subtraction = Subtraction(user_id=1, inputs=[10])
    with pytest.raises(ValueError, match="at least two numbers"):
        subtraction.get_result()


def test_polymorphic_list_of_calculations():
    """Test that different calculation types can be stored in same list."""
    calculations = [
        Calculation.create('addition', 1, [1, 2, 3]),
        Calculation.create('subtraction', 1, [10, 3]),
        Calculation.create('multiplication', 1, [2, 3, 4]),
        Calculation.create('division', 1, [100, 5]),
    ]
    
    assert isinstance(calculations[0], Addition)
    assert isinstance(calculations[1], Subtraction)
    assert isinstance(calculations[2], Multiplication)
    assert isinstance(calculations[3], Division)
    
    results = [calc.get_result() for calc in calculations]
    assert results == [6, 7, 24, 20]


def test_polymorphic_method_calling():
    """Test polymorphic methods work correctly."""
    calc_types = ['addition', 'subtraction', 'multiplication', 'division']
    inputs = [10, 2]
    expected = [12, 8, 20, 5]
    
    for calc_type, expected_result in zip(calc_types, expected):
        calc = Calculation.create(calc_type, 1, inputs)
        result = calc.get_result()
        assert result == expected_result, f"{calc_type} failed: expected {expected_result}, got {result}"



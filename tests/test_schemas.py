import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserCreate, UserRead

def test_usercreate_valid():
    data = {
        "username": "jorge_01",
        "email": "jorge@example.com",
        "password": "Str0ngP@ss!"
    }
    obj = UserCreate(**data)
    assert obj.username == "jorge_01"
    assert obj.email == "jorge@example.com"

def test_usercreate_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="jorge", email="not-an-email", password="Str0ngP@ss!")

def test_usercreate_weak_password_rejected():
    # Adjust if your password validator uses different logic
    with pytest.raises(ValidationError):
        UserCreate(username="jorge", email="j@e.com", password="abc")

def test_usercreate_username_rules():
    # Adjust this if your schema allows spaces
    with pytest.raises(ValidationError):
        UserCreate(username="bad name", email="j@e.com", password="Goodpass1!")

def test_userread_omits_sensitive_fields():
    obj = UserRead(
        id=1,
        username="jorge",
        email="jorge@example.com",
        created_at=datetime.utcnow()
    )
    dumped = obj.model_dump()
    assert "password" not in dumped
    assert "password_hash" not in dumped
    assert dumped["username"] == "jorge"
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserCreate, UserRead

def test_usercreate_valid():
    data = {
        "username": "jorge_01",
        "email": "jorge@example.com",
        "password": "Str0ngP@ss!"
    }
    obj = UserCreate(**data)
    assert obj.username == "jorge_01"
    assert obj.email == "jorge@example.com"

def test_usercreate_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="jorge", email="not-an-email", password="Str0ngP@ss!")

def test_usercreate_weak_password_rejected():
    # Adjust if your password validator uses different logic
    with pytest.raises(ValidationError):
        UserCreate(username="jorge", email="j@e.com", password="abc")

def test_usercreate_username_rules():
    # Adjust this if your schema allows spaces
    with pytest.raises(ValidationError):
        UserCreate(username="bad name", email="j@e.com", password="Goodpass1!")

def test_userread_omits_sensitive_fields():
    obj = UserRead(
        id=1,
        username="jorge",
        email="jorge@example.com",
        created_at=datetime.utcnow()
    )
    dumped = obj.model_dump()
    assert "password" not in dumped
    assert "password_hash" not in dumped
    assert dumped["username"] == "jorge"

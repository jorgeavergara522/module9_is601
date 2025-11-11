import re
from app.auth.security import hash_password, verify_password

def test_hash_and_verify_password():
    raw = "Str0ngP@ss!"
    hashed = hash_password(raw)
    assert hashed != raw, "Hash should never equal the raw password"
    assert verify_password(raw, hashed) is True
    assert verify_password("wrong-pass", hashed) is False

def test_hash_is_not_plaintext_or_short():
    raw = "anotherGood1!"
    hashed = hash_password(raw)
    assert hashed.startswith("$2"), "Expected bcrypt-style hash"
    assert len(hashed) > 50

def test_same_password_hashes_differ_due_to_salt():
    raw = "SamePass123!"
    h1 = hash_password(raw)
    h2 = hash_password(raw)
    assert h1 != h2, "Hashes for same password should differ due to salt"
    assert verify_password(raw, h1)
    assert verify_password(raw, h2)

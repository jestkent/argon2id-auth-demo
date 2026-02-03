from app.auth import hash_password, verify_password

def test_hash_and_verify():
    h = hash_password("StrongPass123!")
    ok, upgraded = verify_password(h, "StrongPass123!")
    assert ok is True
    assert upgraded is None

def test_wrong_password():
    h = hash_password("StrongPass123!")
    ok, _ = verify_password(h, "WrongPass123!")
    assert ok is False

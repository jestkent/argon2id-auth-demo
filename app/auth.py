from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from .config import SECURITY

# PasswordHasher uses Argon2id by default in argon2-cffi
ph = PasswordHasher(
    time_cost=SECURITY.time_cost,
    memory_cost=SECURITY.memory_cost,
    parallelism=SECURITY.parallelism,
)

def hash_password(plain_password: str) -> str:
    if len(plain_password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    return ph.hash(plain_password)

def verify_password(stored_hash: str, plain_password: str) -> tuple[bool, str | None]:
    """
    Returns (is_valid, upgraded_hash_or_none).
    If valid and params are outdated, returns upgraded hash.
    """
    try:
        ok = ph.verify(stored_hash, plain_password)
    except VerifyMismatchError:
        return False, None

    # If the hash was generated with weaker params, upgrade it
    if ok and ph.check_needs_rehash(stored_hash):
        return True, ph.hash(plain_password)

    return True, None

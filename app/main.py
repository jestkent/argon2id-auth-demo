from fastapi import FastAPI, HTTPException, Request
from .db import init_db, create_user, get_user_by_username, update_password_hash
from .auth import hash_password, verify_password
from .models import RegisterRequest, LoginRequest
from .rate_limit import SimpleRateLimiter

app = FastAPI(title="Argon2id Auth Demo")
limiter = SimpleRateLimiter(max_requests=10, window_seconds=60)

@app.on_event("startup")
def startup():
    init_db()

@app.post("/register")
def register(body: RegisterRequest):
    existing = get_user_by_username(body.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")

    try:
        pw_hash = hash_password(body.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    create_user(body.username, pw_hash)
    return {"ok": True, "message": "User registered"}

@app.post("/login")
def login(request: Request, body: LoginRequest):
    ip = request.client.host if request.client else "unknown"
    key = f"login:{ip}:{body.username}"

    if not limiter.allow(key):
        raise HTTPException(status_code=429, detail="Too many attempts. Try again later.")

    user = get_user_by_username(body.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    valid, upgraded_hash = verify_password(user["password_hash"], body.password)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if upgraded_hash:
        update_password_hash(user["id"], upgraded_hash)

    # For demo only. In real apps, return a session or JWT.
    return {"ok": True, "message": "Login successful", "rehash_upgraded": bool(upgraded_hash)}

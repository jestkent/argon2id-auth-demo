from fastapi import FastAPI, HTTPException, Request
from .db import init_db, create_user, get_user_by_username, update_password_hash
from .auth import hash_password, verify_password
from .models import RegisterRequest, LoginRequest
from .rate_limit import SimpleRateLimiter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .server_log import add_event, get_events
from .config import SECURITY



app = FastAPI(title="Argon2id Auth Demo")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

limiter = SimpleRateLimiter(max_requests=10, window_seconds=60)

@app.on_event("startup")
def startup():
    init_db()

@app.post("/register")
def register(body: RegisterRequest):
    existing = get_user_by_username(body.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")

    pw_hash = hash_password(body.password)
    create_user(body.username, pw_hash)

    # NEW: log what the server did (demo only)
    add_event({
        "action": "register",
        "username": body.username,
        "argon2id_params": {
            "memory_cost_kib": SECURITY.memory_cost,
            "time_cost": SECURITY.time_cost,
            "parallelism": SECURITY.parallelism
        },
        "db_action": "INSERT user",
        "hash_prefix": pw_hash[:60] + "...",
        "message": "Password hashed with Argon2id. Plaintext password never stored."
    })

    return {"ok": True, "message": "User registered"}

@app.post("/login")
def login(request: Request, body: LoginRequest):
    ip = request.client.host if request.client else "unknown"
    key = f"login:{ip}:{body.username}"

    if not limiter.allow(key):
        raise HTTPException(status_code=429, detail="Too many attempts")

    user = get_user_by_username(body.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    valid, upgraded_hash = verify_password(user["password_hash"], body.password)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db_action = "NO CHANGE"
    hash_prefix = user["password_hash"][:60] + "..."

    if upgraded_hash:
        update_password_hash(user["id"], upgraded_hash)
        db_action = "UPDATE password_hash"
        hash_prefix = upgraded_hash[:60] + "..."

    # NEW: log what the server did (demo only)
    add_event({
        "action": "login",
        "username": body.username,
        "argon2id_params": {
            "memory_cost_kib": SECURITY.memory_cost,
            "time_cost": SECURITY.time_cost,
            "parallelism": SECURITY.parallelism
        },
        "rehash_upgraded": bool(upgraded_hash),
        "db_action": db_action,
        "hash_prefix": hash_prefix,
        "message": "Password verified against stored hash. Plaintext password never stored."
    })

    return {
        "ok": True,
        "message": "Login successful",
        "rehash_upgraded": bool(upgraded_hash)
    }



@app.get("/explain/{username}")
def explain(username: str):
    """
    Demo-only endpoint.
    Returns safe, partial info so you can explain Argon2id without exposing secrets.
    """
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stored_hash = user["password_hash"]

    # Only show a prefix, never the full hash
    # This is enough to prove Argon2id + parameters exist
    hash_prefix = stored_hash[:60] + "..." if len(stored_hash) > 60 else stored_hash

    return {
        "username": user["username"],
        "hash_prefix": hash_prefix,
        "note": "Demo only: passwords are never stored or displayed. Only a hash prefix is shown."
    }
@app.get("/server-log")
def server_log():
    return {"events": get_events()}


#
##
# To run the app, use:
# D:\Desktop\argon2id-auth-demo>uvicorn app.main:app --reload
##
#
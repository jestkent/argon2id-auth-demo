# Argon2id Auth Demo (Educational)

A small FastAPI project that demonstrates secure password hashing using **Argon2id** and an educational split UI that shows what the backend is doing (safely).

## Why this exists
This project is built to demonstrate practical understanding of:
- Password hashing with **Argon2id** (memory-hard)
- Safe storage (never plaintext passwords)
- Verification flow (hash check, no decryption)
- Rehash-on-login (upgrade hashes when parameters improve)
- Rate limiting to slow brute-force attempts
- Clear “client vs server” educational visualization

## Features
- Register and login API endpoints
- Argon2id hashing via `argon2-cffi`
- SQLite storage
- Demo-only server log endpoint for educational purposes
- Split UI:
  - Client-side form inputs
  - Server-side explanation panel (hash prefix, parameters, DB actions)

## Run locally (Windows / PowerShell)
```powershell
cd argon2id-auth-demo
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

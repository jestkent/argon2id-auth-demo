# Argon2id Auth Demo

A small FastAPI project demonstrating secure password hashing using Argon2id via argon2-cffi.

## Features
- Register: hashes passwords with Argon2id
- Login: verifies password without ever decrypting anything
- Rehash upgrade: automatically rehashes on login if parameters are outdated
- Basic rate limiting on login attempts
- SQLite storage

## Why Argon2id
Argon2id is a memory-hard password hashing algorithm designed to resist GPU/ASIC brute-force attacks. It includes per-password salts and supports tunable parameters.

## Run
pip install -r requirements.txt  
uvicorn app.main:app --reload

## Endpoints
POST /register  
POST /login

## Notes
- For demo purposes only: /login returns a simple success JSON. In a real system you would issue a session or token.
- Rate limiting is in-memory. Production should use Redis or an API gateway.

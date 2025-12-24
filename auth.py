import os
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_SECRET_KEY = os.getenv("API_SECRET_KEY")

if not API_SECRET_KEY:
    raise RuntimeError("API_SECRET_KEY is not set in environment variables.")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
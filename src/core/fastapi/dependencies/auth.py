from fastapi import HTTPException
from src.core.config import CONFIG
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Define the security scheme
security_scheme = HTTPBearer()

async def authenticate_user(credentials: HTTPAuthorizationCredentials = Security(security_scheme)):
    # Validate and extract the token from the credentials
    token = credentials.credentials
    # Replace this with your own authentication logic
    if not token or token != CONFIG.BEARER:
        raise HTTPException(status_code=401, detail="Unauthorized")

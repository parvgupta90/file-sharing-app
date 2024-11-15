import logging
from fastapi import HTTPException
import jwt
from datetime import datetime, timedelta

import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of log output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to the console
        logging.FileHandler("service_debug.log")  # Log to a file for persistent storage
    ]
)

logger = logging.getLogger(__name__)


SECRET_KEY = "jtUHX6TPf9se0wtbd5fkEjG5oK7wcyGdO-d11LnA-zg"
ALGORITHM = "HS256"

def create_jwt_token(username: str, role: str = "user"):
    logger.debug("Creating JWT token for user: %s with role: %s", username, role)
    payload = {
        "sub": username,
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug("JWT token created: %s", token)
    return token

def verify_token(token: str):
    try:
        print("Verifying token...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token verified successfully.")
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token.")
        raise HTTPException(status_code=401, detail="Invalid token")


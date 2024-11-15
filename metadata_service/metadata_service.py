from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt  # Ensure PyJWT is installed
import os
import json

app = FastAPI()

# In-memory metadata store (can use file-based storage for persistence)
METADATA_FILE = "metadata.json"

# JWT Secret and Algorithm
SECRET_KEY = "jtUHX6TPf9se0wtbd5fkEjG5oK7wcyGdO-d11LnA-zg"  # Replace with your actual JWT secret key
ALGORITHM = "HS256"
security = HTTPBearer()

# Utility functions for file-based metadata persistence
def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_metadata_to_file(data):
    with open(METADATA_FILE, "w") as file:
        json.dump(data, file)

file_metadata = load_metadata()

# Dependency to verify JWT token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return payload if the token is valid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

class Metadata(BaseModel):
    filename: str
    location: str

@app.post("/save_metadata/")
async def save_metadata(metadata: Metadata, token_payload: dict = Depends(verify_token)):
    print(f"Token payload: {token_payload}")
    if metadata.filename in file_metadata:
        raise HTTPException(status_code=400, detail="File metadata already exists")

    file_metadata[metadata.filename] = metadata.location
    save_metadata_to_file(file_metadata)
    return {"message": "Metadata saved successfully", "metadata": metadata.dict()}

@app.get("/get_metadata/{filename}")
async def get_metadata(filename: str, token_payload: dict = Depends(verify_token)):
    if filename in file_metadata:
        return {"filename": filename, "location": file_metadata[filename]}
    else:
        raise HTTPException(status_code=404, detail="File metadata not found")

@app.post("/token/")
async def generate_token():
    payload = {
        "sub": "test_user",
        "role": "user",
        "exp": 3600  # Set token expiration (e.g., in seconds)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

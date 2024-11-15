from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt  # Ensure PyJWT is installed
from urllib.parse import unquote

app = FastAPI()

UPLOAD_DIRECTORY = "/uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

SECRET_KEY = "jtUHX6TPf9se0wtbd5fkEjG5oK7wcyGdO-d11LnA-zg"
ALGORITHM = "HS256"
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/download/{filename}")
async def download_file(filename: str, token_payload: dict = Depends(verify_token)):
    decoded_filename = unquote(filename)
    file_path = os.path.join(UPLOAD_DIRECTORY, decoded_filename)

    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=decoded_filename, media_type='application/octet-stream')
    else:
        raise HTTPException(status_code=404, detail="File not found")

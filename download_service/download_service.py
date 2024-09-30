from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
from urllib.parse import unquote

app = FastAPI()

# Ensure the upload directory is the same across services
UPLOAD_DIRECTORY = "/app/uploads"

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.get("/download/{filename}")
async def download_file(filename: str):
    # Decode the filename in case it contains special characters
    decoded_filename = unquote(filename)
    file_path = os.path.join(UPLOAD_DIRECTORY, decoded_filename)

    # Check if the file exists
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=decoded_filename, media_type='application/octet-stream')
    else:
        raise HTTPException(status_code=404, detail="File not found")

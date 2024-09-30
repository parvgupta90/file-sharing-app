from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any ori`gin (use specific URLs in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "uploads/")

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"{UPLOAD_DIRECTORY}{file.filename}"
        print(f"Saving file to: {file_location}")
        
        # Ensure the directory exists
        if not os.path.exists(UPLOAD_DIRECTORY):
            print(f"Directory {UPLOAD_DIRECTORY} does not exist, creating it now.")
            os.makedirs(UPLOAD_DIRECTORY)
        else:
            print(f"Directory {UPLOAD_DIRECTORY} already exists.")
        
        # Save the file to disk
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
            print(f"File saved successfully at {file_location}")

        # Check if file exists after saving
        if os.path.exists(file_location):
            print(f"File {file_location} exists after saving.")
        else:
            print(f"File {file_location} does NOT exist after saving!")

        # Metadata service request (assuming it's working)
        metadata_response = requests.post(
            "http://metadata_service:8002/save_metadata/",
            json={"filename": file.filename, "location": file_location}
        )

        if metadata_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to save metadata")

        return {"message": "File uploaded successfully", "metadata": metadata_response.json()}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/uploads")
async def get_uploaded_files():
    try:
        files = os.listdir(UPLOAD_DIRECTORY)
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
    else:
        raise HTTPException(status_code=404, detail="File not found")

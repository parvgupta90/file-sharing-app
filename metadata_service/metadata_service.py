# from fastapi import FastAPI
# from pymongo import MongoClient

# app = FastAPI()

# # MongoDB setup
# client = MongoClient("mongodb://localhost:27017/")
# db = client['file_storage']
# metadata_collection = db['metadata']

# @app.post("/save_metadata/")
# def save_metadata(file_name: str, file_location: str):
#     metadata = {"file_name": file_name, "file_location": file_location}
#     metadata_collection.insert_one(metadata)
#     return {"message": "Metadata saved successfully"}

# @app.get("/get_metadata/{file_name}")
# def get_metadata(file_name: str):
#     metadata = metadata_collection.find_one({"file_name": file_name})
#     if metadata:
#         return metadata
#     return {"error": "File not found"}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory metadata store (replace with a database in production)
file_metadata = {}

class Metadata(BaseModel):
    filename: str
    location: str

@app.post("/save_metadata/")
async def save_metadata(metadata: Metadata):
    if metadata.filename in file_metadata:
        raise HTTPException(status_code=400, detail="File metadata already exists")
    file_metadata[metadata.filename] = metadata.location
    return {"message": "Metadata saved successfully", "metadata": metadata.dict()}

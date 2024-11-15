from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import requests
import uuid
import smtplib
from email.mime.text import MIMEText
from auth_utils import verify_token
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "uploads")
PUBLIC_LINKS_DIRECTORY = os.path.join(os.getcwd(), "public_links")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(PUBLIC_LINKS_DIRECTORY, exist_ok=True)

# Define models for the request bodies
class GenerateLinkRequest(BaseModel):
    filename: str

class ShareableLinkRequest(BaseModel):
    filename: str
    recipient_email: EmailStr

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload.get("username"), token

@app.post("/uploads")
async def upload_file(file: UploadFile = File(...), current_user_and_token: tuple = Depends(get_current_user)):
    current_user, token = current_user_and_token
    file_location = os.path.join(UPLOAD_DIRECTORY, f"{current_user}_{file.filename}")

    try:
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # Optional: Call metadata service if available
        requests.post(
            "http://metadata_service:8002/save_metadata/",
            json={"filename": file.filename, "location": file_location},
            headers={"Authorization": f"Bearer {token}"}
        )

        return {"message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/generate-link")
async def generate_shareable_link(
    request: GenerateLinkRequest, 
    current_user_and_token: tuple = Depends(get_current_user)
):
    current_user, _ = current_user_and_token
    filename = request.filename
    user_file_path = os.path.join(UPLOAD_DIRECTORY, f"{current_user}_{filename}")
 # Debugging statements
    try:
        print(f"User file path: {user_file_path}")
        print(f"Link path: {link_path}")
    except Exception as e:
        print(f"Debug printing error: {e}")
    # Check if file exists
    if not os.path.exists(user_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Generate unique link ID
    link_id = str(uuid.uuid4())
    link_path = os.path.join(PUBLIC_LINKS_DIRECTORY, f"{link_id}_{filename}")

    # Create a symbolic link to the original file
    os.symlink(user_file_path, link_path)

    # Return the public URL for the file
    public_url = f"http://localhost:8001/public/{link_id}_{filename}"
    return {"public_url": public_url}
    

@app.post("/share-via-email")
async def share_file_via_email(
    request: ShareableLinkRequest,
    current_user_and_token: tuple = Depends(get_current_user)
):
    current_user, _ = current_user_and_token
    filename = request.filename
    recipient_email = request.recipient_email

    # Define the path to the user's file
    user_file_path = os.path.join(UPLOAD_DIRECTORY, f"{current_user}_{filename}")

    # Check if the file exists
    if not os.path.exists(user_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Generate a unique link ID and create the public link path
    link_id = str(uuid.uuid4())
    link_path = os.path.join(PUBLIC_LINKS_DIRECTORY, f"{link_id}_{filename}")
    
    # Create a symbolic link to the original file for sharing
    os.symlink(user_file_path, link_path)

    # Generate the public URL for the file
    public_url = f"http://localhost:8001/public/{link_id}_{filename}"

    # SMTP configuration
    smtp_server = "smtp-relay.brevo.com"  # SendinBlue/Brevo SMTP server
    port = 587  # TLS port
    sender_email = "parv.gupta90@brevo.com"
    api_key = "your_api_key_here"

    # Construct the email message
    msg = MIMEText(f"Hello,\n\nA file has been shared with you. Access it here: {public_url}")
    msg["Subject"] = "File Shared with You"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        # Send the email using SMTP
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, api_key)  # Authenticate using the API key as password
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        # Return a success message along with the public URL
        return {"message": "File link shared via email successfully", "public_url": public_url}
    except Exception as e:
        # Handle any exceptions and provide an appropriate HTTP error
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@app.get("/uploads")
async def list_files(current_user_and_token: tuple = Depends(get_current_user)):
    current_user, _ = current_user_and_token
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        if filename.startswith(f"{current_user}_"):
            # Strip `current_user` prefix for display
            display_filename = filename.replace(f"{current_user}_", "")
            file_size = os.path.getsize(os.path.join(UPLOAD_DIRECTORY, filename))
            files.append({
                "name": display_filename,
                "size": file_size
            })
    return files

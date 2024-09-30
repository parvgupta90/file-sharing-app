
# File Upload & Management System

## Overview

This project is a **File Upload & Management System** built using **FastAPI**, **Docker**, and **Bootstrap**. It allows users to upload files via a web interface, view the list of uploaded files, and download them. The system is designed using microservices architecture, with separate services handling file uploads, metadata storage, and file downloads.

## Technology Stack
- **Backend**: FastAPI
- **Frontend**: HTML, Bootstrap, JavaScript
- **Containerization**: Docker, Docker Compose
- **Storage**: Local file system (extendable to cloud or database storage)
- **Microservices**: Upload service, metadata service, download service

## System Architecture

The system is divided into three microservices:
1. **Upload Service**: Handles file uploads and saves metadata to the metadata service.
2. **Metadata Service**: Stores file metadata (e.g., file name, location) in memory.
3. **Download Service**: Handles file downloads by serving files from the shared directory.

---

## How to Run the Project

### Prerequisites
- **Docker**: Ensure Docker is installed on your machine.
- **Docker Compose**: This is needed to manage the services and volumes.

### Steps to Run the Project

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd file-sharing-app
   ```

2. **Build and Start the Services**
   ```bash
   docker-compose up --build
   ```

3. **Access the Web Interface**
   - The file upload service is accessible at: `http://localhost:8001`
   - Uploaded files can be accessed and downloaded at: `http://localhost:8003/uploads`

4. **Upload Files**
   - Select a file and click "Upload" on the web interface.
   - After a successful upload, you will see the list of uploaded files.

5. **Download Files**
   - Navigate to the **Uploaded Files** tab on the web interface.
   - You can download any file by clicking the **Download** button next to the file name.

## Project Structure

```
├── docker-compose.yml         # Docker Compose file
├── upload_service             # Upload service code
│   ├── Dockerfile             # Dockerfile for upload service
│   └── upload_service.py      # FastAPI app for file uploads
├── download_service           # Download service code
│   ├── Dockerfile             # Dockerfile for download service
│   └── download_service.py    # FastAPI app for file downloads
├── metadata_service           # Metadata service code
│   ├── Dockerfile             # Dockerfile for metadata service
│   └── metadata_service.py    # FastAPI app for managing metadata
├── templates                  # HTML templates for the web interface
│   └── index.html             # Main HTML template
└── uploads                    # Directory where uploaded files are stored
```

## Future Enhancements
- **Authentication**: Implement user authentication to secure file uploads and downloads.
- **Metadata Storage**: Extend the metadata service to use a database like MongoDB or PostgreSQL.
- **Cloud Storage**: Enable cloud storage options such as AWS S3 for scalable file storage.

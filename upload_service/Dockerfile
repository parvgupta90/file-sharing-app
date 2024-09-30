# # Use the official Python image as the base
# # FROM python:3.12-slim

# # Set the working directory
# WORKDIR /app

# # Copy and install requirements
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application
# COPY . .

# # Expose the port the app runs on
# EXPOSE 8001

# # Command to run the application
# CMD ["uvicorn", "upload_service:app", "--reload", "--port", "8001"]
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "upload_service:app", "--host", "0.0.0.0", "--port", "8001"]

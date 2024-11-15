# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Ensure that the Python path includes the current directory for proper module imports
ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 8001

# Command to run the application with Uvicorn
CMD ["uvicorn", "upload_service:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

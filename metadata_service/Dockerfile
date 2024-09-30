# # Use Python 3.9 as the base image
# FROM python:3.9-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install the dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose the port for the metadata service
# EXPOSE 8002

# # Command to run the metadata service
# CMD ["uvicorn", "metadata_service:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["uvicorn", "metadata_service:app", "--host", "0.0.0.0", "--port", "8002"]

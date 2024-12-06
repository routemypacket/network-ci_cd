# Use a Python base image
FROM python:3.10-slim

# Install necessary utilities (including curl)
RUN apt-get update && apt-get install -y --no-install-recommends curl

# Set the working directory
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

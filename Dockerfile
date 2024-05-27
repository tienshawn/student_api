# Use the official Python 3.8 slim image as the base image
FROM python:3.10-slim

# Set the working directory within the container
WORKDIR /api

# Copy the necessary files and directories into the container
COPY .env app.py requirements.txt  /api/

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the Flask application using Gunicorn
CMD ["gunicorn", "app:application", "-b", "0.0.0.0:5000", "-w", "4"]
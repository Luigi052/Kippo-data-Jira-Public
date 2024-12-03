# Use an official Python runtime as a parent image
FROM python:3.9-slim
LABEL authors="luigi"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME=Jira-API

# Run app.py when the container launches
CMD ["python", "main.py"]



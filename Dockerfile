# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install -r requirements.txt

# Make port 8766 available to the world outside this container
EXPOSE 8766

# Run websocket_server.py when the container launches
CMD ["python", "websocket_server.py"]

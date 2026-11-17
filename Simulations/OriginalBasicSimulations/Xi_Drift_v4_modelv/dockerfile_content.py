# Generate Dockerfile for the Dash app

dockerfile_content = """
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install dash numpy matplotlib plotly

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Run app.py when the container launches
CMD ["python", "model5_dashboard_full.py"]
"""

# Save Dockerfile
dockerfile_path = "/mnt/data/Dockerfile"
with open(dockerfile_path, "w", encoding="utf-8") as f:
    f.write(dockerfile_content)

# Generate docker-compose.yml
docker_compose_content = """
version: '3'
services:
  model5-dashboard:
    build: .
    ports:
      - "8050:8050"
    volumes:
      - .:/app
    environment:
      - DASH_DEBUG_MODE=True
"""

# Save docker-compose.yml
compose_path = "/mnt/data/docker-compose.yml"
with open(compose_path, "w", encoding="utf-8") as f:
    f.write(docker_compose_content)

dockerfile_path, compose_path

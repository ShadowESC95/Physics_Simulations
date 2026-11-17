
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

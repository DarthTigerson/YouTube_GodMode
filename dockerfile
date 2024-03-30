# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install PDM
RUN pip install pdm

# Copy the project files into the container at /app
COPY . .

# Make sure run.sh is executable
RUN chmod +x run.sh

# Install project dependencies
RUN pdm install --prod

# Expose the port the app runs on
EXPOSE 8000

# Use the run.sh script to start the service
CMD ["./run.sh"]

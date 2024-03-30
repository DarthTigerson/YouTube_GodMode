# Use an official lightweight Python image
FROM python:3.12-slim

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

# Install project dependencies
RUN pdm install --prod

# Document that the service listens on port 8000
EXPOSE 8000

# Start the Uvicorn server
CMD ["pdm", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

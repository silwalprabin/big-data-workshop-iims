# Use a Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the script into the container
COPY kafka_producer.py .

# Install required dependencies
RUN pip install kafka-python

# Set the command to run the producer script
CMD ["python", "kafka_producer.py"]

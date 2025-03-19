# Use the official Python base image
FROM python:3.11.0-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the main.py file to the working directory
COPY main.py .

# Install the requests library 
RUN pip install requests

# Run the main.py file using Python
CMD ["python", "main.py"]
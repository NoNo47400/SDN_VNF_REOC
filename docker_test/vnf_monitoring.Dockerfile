# Use the official Python image based on Alpine
FROM python:3.9-alpine

# Set the working directory
WORKDIR /usr/src/app

RUN apk add --no-cache bash

RUN pip install --upgrade pip

# Install Flask and Requests directly using pip
RUN pip install --no-cache-dir flask requests 

# Copy the Flask script into the container
COPY monitoring_vnf.py .

# Expose the port used by the Flask application
EXPOSE 8181

# Define the command to run the Flask file
CMD ["python", "monitoring_vnf.py"]
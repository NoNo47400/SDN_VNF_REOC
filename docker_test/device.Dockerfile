# Use the official Node.js image based on Alpine
FROM node:alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy the JavaScript program file into the container
COPY device.js .

# Command to run the application
CMD ["node", "device.js", "--local_ip", "0.0.0.0", "--local_port", "9001", "--local_name", "${DEVICE_NAME}", "--remote_ip", "127.0.0.1", "--remote_port", "8282", "--remote_name", "gwf1", "--send_period", "3000"]

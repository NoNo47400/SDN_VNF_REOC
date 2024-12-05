# Use the official Node.js image based on Alpine
FROM node:alpine

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
RUN npm install express
RUN npm install request
RUN npm install systeminformation
RUN npm install yargs

# Copy the JavaScript program file into the container
COPY application.js .

# Command to run the application
CMD ["node", "application.js", "--remote_ip", "0.0.0.0", "--remote_port", "8080", "--device_name", "${APP_DEVICE_NAME}", "--send_period", "5000"]

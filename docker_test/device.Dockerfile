# Use the official Node.js image based on Alpine
FROM node:alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy the JavaScript program file into the container
COPY Device.js .

# Command to run the application
CMD ["node", "Device.js"]

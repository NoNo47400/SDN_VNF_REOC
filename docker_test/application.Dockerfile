# Use the official Node.js image based on Alpine
FROM node:alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy the JavaScript program file into the container
COPY Application.js .

# Command to run the application
CMD ["node", "Application.js"]

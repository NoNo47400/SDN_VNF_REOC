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
COPY gateway.js .

# Command to run the application
CMD ["node", "gateway.js", "--local_ip", "127.0.0.1", "--local_port", "8181", "--local_name", "${GWI_NAME}", "--remote_ip", "127.0.0.1", "--remote_port", "8080", "--remote_name", "srv"]

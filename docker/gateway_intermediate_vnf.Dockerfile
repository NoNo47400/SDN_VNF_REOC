# Use the official Node.js image based on Alpine
FROM node:alpine

# Set the working directory
WORKDIR /usr/src/app

RUN npm update
RUN npm audit fix

# Install dependencies
RUN npm install express
RUN npm install request
RUN npm install systeminformation
RUN npm install yargs

# Install bash (necessary for debugging or running commands interactively)
RUN apk add --no-cache bash curl tcpdump

EXPOSE 8181

# Copy the JavaScript program file into the container
COPY gateway.js .

# Command to run the application
CMD ["node", "gateway.js", "--local_ip", "0.0.0.0", "--local_port", "8181", "--local_name", "gwi2", "--remote_ip", "10.0.0.100", "--remote_port", "8080", "--remote_name", "srv"]
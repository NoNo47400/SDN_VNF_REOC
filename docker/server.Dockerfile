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

EXPOSE 8080

# Copy the JavaScript program file into the container
COPY server.js .

# Command to run the server
#CMD ["node", "server.js", "--local_ip", "0.0.0.0", "--local_port", "8080", "--local_name", ${SRV_NAME}]
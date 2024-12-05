# Use the official Node.js image based on Alpine
FROM node:alpine

# Set the working directory
WORKDIR /usr/src/app

# Install npm dependencies
RUN npm install

# Set an environment variable
ENV VAR="valeur default"

# Set the command to run the application
CMD ["node", "$VAR"]

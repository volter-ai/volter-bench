# Use Node.js slim Buster as the base image
FROM node:14-slim as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the necessary folders and files
COPY assets ./assets
COPY public ./public
COPY src ./src
COPY deploy/*.tf ./deploy/

# Build the React app
RUN npm run build

# Start a new stage for a smaller final image
FROM node:14-slim

ENV PORT=8000

WORKDIR /app

# Install serve for running the application
RUN npm install -g serve

# Copy the build output from the previous stage
COPY --from=build /app/deploy ./deploy

# Command to run the application using the PORT environment variable
CMD serve -s -l tcp://0.0.0.0:$PORT deploy/dist
# AI Employee Project

## Overview

The AI Employee project is an AI-powered tool designed for efficient data analysis and comprehensive report generation. It integrates various components, including data processing, analysis engines, and report generation modules, into a unified system accessible via both a Command-Line Interface (CLI) and a web-based interface. This README provides instructions for setting up and running the project using Docker.

## Prerequisites

Before you start, ensure you have the following installed on your system:

- [Docker](https://www.docker.com/products/docker-desktop): For containerization.
- [Docker Compose](https://docs.docker.com/compose/): For managing multi-container Docker applications.

## Project Structure

The project directory includes the following components:

- `app/`: Contains the application code.
  - `cli/`: CLI scripts for interacting with the system.
  - `nlp/`: NLP utilities for processing user queries.
  - `routes/`: FastAPI routes for handling API requests.
- `tests/`: Unit tests for validating the functionality of various modules.
- `docs/`: Documentation files.
- `Dockerfile`: Defines the Docker image for the application.
- `docker-compose.yml`: Defines the services, networks, and volumes for the Docker environment.
- `requirements.txt`: Lists the Python dependencies for the project.

## Getting Started with Docker

Follow these steps to set up and run the AI Employee project using Docker:

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/Sukhpreet2001/ai-employee.git
cd ai-employee
# AI Employee Project

## Getting Started with Docker

### 2. Build the Docker Image

Build the Docker image using the provided `Dockerfile`:

```bash
docker build -t ai-employee .

### 2. Build the Docker Image
Start the application and its dependencies using Docker Compose:
```bash
docker-compose up
This command will:

Build the Docker images (if not already built).
Create and start the containers defined in docker-compose.yml.
Make the application available at http://localhost:8000 for the web interface.
Provide CLI access.

###3. Accessing the Application
Web Interface: Open your web browser and navigate to http://localhost:8000 to access the web interface.

CLI Interface: You can interact with the CLI within the running Docker container. Use the following command to open a shell in the CLI container:
```bash
docker-compose exec cli bash
From the shell, you can run CLI commands such as:
```bash
python app/cli/cli.py query

###4. Stopping the Docker Containers
To stop the running Docker containers, use:
```bash
docker-compose down
This command will stop and remove the containers, networks, and volumes defined in the docker-compose.yml file.

###Configuration
The configuration for the application is specified in the docker-compose.yml file. You can adjust environment variables and other settings as needed.

###Testing
To run the unit tests for the project, execute the following command:
```bash
docker-compose exec app pytest

This command runs the tests within the app container.

###Troubleshooting
Port Conflicts: Ensure that port 8000 is not in use by other applications.
File Permissions: Check that Docker has the necessary permissions to read and write files on your system.


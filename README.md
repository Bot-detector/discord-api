# Bot Detector - Discord API - Local Development Environment Setup

This repository contains a MySQL database and a FastAPI API for the Discord Bot Detector. You can use Docker Compose to set up your local development environment with ease.

## Prerequisites

Before you begin, ensure that you have the following installed on your machine:

- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)
- Python: [Installation Guide](https://www.python.org/downloads/)
- Git: [Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Getting Started

To set up your local development environment, follow these steps:

1. Clone this repository to your local machine
2. Configure the environment variables for the API:
    - Rename the file `src/.env-example` to `src/.env`

3. Set up Python and install dependencies:
    - Create a virtual environment:
        ```
        python -m venv .venv
        ```
    - if you are using vscode, you should see a popup after this command, you should set the .venv as your default interpreter for this workspace.
    - Activate the virtual environment:
    - On Windows:
        ```
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```
        source .venv/bin/activate
        ```
    - Upgrade pip:
        ```
        python -m pip install --upgrade pip
        ```
    - Install the required packages:
        ```
        pip install -r src/requirements.txt
        ```

4. Start the development environment using Docker Compose:
    ```
    docker-compose up --build
    ```
    **Note:** The `--build` flag is used to ensure that any changes are incorporated into the container.

5. Wait until the MySQL server is ready to accept connections. 
    - You will see a message in the terminal that says `*/usr/sbin/mysqld: ready for connections.*`. 
    - This may take a few moments.

6. Test the development environment by accessing the following URL in your web browser: [http://localhost:3000/docs](http://localhost:3000/docs).
    - Use the bearer token provided in the `src/.env` file for authentication.
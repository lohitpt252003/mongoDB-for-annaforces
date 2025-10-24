# MongoDB Setup for Annaforces

This repository contains the configuration for running a MongoDB database, a Mongo Express admin interface, and an automatic database initializer using Docker Compose.

## Prerequisites

- Docker and Docker Compose

## Getting Started

### 1. Environment Variables
This project uses a `.env` file to manage configuration. The file is pre-configured with default values, which you can modify if needed.

```
# MongoDB Credentials
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example

# Mongo Express Credentials
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=password
```

### 2. Start the Services
Run the following command to build the initialization container and start all services:
```bash
docker-compose up --build -d
```
The `--build` flag is only necessary the first time or after changing the initialization script.

## Database Initialization
The database initialization is now handled automatically by the `db-init` service. When the services start, a script runs which creates the `data` database and the following collections and indexes:

-   **`users` collection:** The `username` is the primary key (`_id`).
    -   Unique index on `email`.
-   **`problems` collection:**
    -   Index on `difficulty`.
    -   Index on `tags`.
-   **`submissions` collection:**
    -   Index on `username`.
    -   Index on `problem_id`.
    -   Index on `verdict`.
    -   Compound index on `(username, problem_id)`.
    -   Compound index on `(username, verdict)`.
    -   Compound index on `(problem_id, verdict)`.
-   **`submissions_queue` collection:**
    -   Unique index on `submission_id`.
## Services

### MongoDB
-   **Host:** `localhost`
-   **Port:** `27017`
-   **Username:** `root`
-   **Password:** `example`

### Mongo Express
-   **URL:** [http://localhost:8081](http://localhost:8081)
-   **Username:** `admin`
-   **Password:** `password`

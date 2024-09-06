# PCM API

## Introduction

This is an API project for PCM, intended for internal use only. It provides backend services and integrations for the PCM platform. The API is built to be secure, scalable, and maintainable, ensuring that it meets the needs of PCM's internal operations.

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository**:

   ```sh
   git clone git@gitlab.com:mi-equipo/pcm.back.git
   cd pcm.back
   ```

2. **Create and configure environment variables**:

   - Create a `.env` file in the root directory of the project and populate it with the necessary environment variables. **Do not commit this file to the repository.** Below is an example of what your `.env` file might look like:

   ```plaintext
   SECRET_KEY=staging_secret_key
   POSTGRES_USER=staging_postgres
   POSTGRES_PASSWORD=staging_postgres_password
   POSTGRES_DB=staging_postgres_db
   PGADMIN_DEFAULT_EMAIL=myslermark@gmail.com
   PGADMIN_DEFAULT_PASSWORD=staging_password
   API_DB_NAME=staging_pcm_db
   API_DB_USER=staging_api_user
   API_DB_PASSWORD=staging_api_password
   BASE_URL=your_api_base_url

   ```

   - Similarly, create a `.env.keycloak` file and populate it with the necessary environment variables for Keycloak:

   ```plaintext
   KC_DB=postgres
   KC_DB_URL=jdbc:postgresql://staging_db/pcm
   KC_DB_USERNAME=staging_db_user
   KC_DB_PASSWORD=staging_db_password
   KC_HOSTNAME=staging_localhost
   KC_HOSTNAME_PORT=8080
   KC_HOSTNAME_STRICT=false
   KC_HOSTNAME_STRICT_HTTPS=false
   KC_LOG_LEVEL=info
   KC_METRICS_ENABLED=true
   KC_HEALTH_ENABLED=true
   KEYCLOAK_ADMIN=staging_keycloak_admin
   KEYCLOAK_ADMIN_PASSWORD=staging_keycloak_password
   KEYCLOAK_REALM_ADMIN=staging_keycloak_realm_admin
   KEYCLOAK_REALM_ADMIN_PASSWORD=staging_keycloak_realm_admin_password
   ```

3. **Build and start the Docker containers**:

   ```sh
   docker compose up --build -d
   ```

4. **Stop the containers**:

   ```sh
   docker-compose down
   ```

## Development Workflow

### Branching Strategy

Develop your features in branches named according to the type of work being done. Here are some examples:

- `feat/your-feature-name` for new features
- `fix/your-bugfix-name` for bug fixes
- `refactor/your-refactor-name` for code refactoring
- `docs/your-documentation-update` for documentation updates
- `tests/your-test-addition` for adding or updating tests
- `chore/your-chore-name` for routine tasks and maintenance

### Creating a Merge Request

1. **Push your branch** to the remote repository:

   ```sh
   git push origin your-branch-name
   ```

2. **Create a Merge Request (MR)** on GitLab. Include links to the relevant User Stories (US) and tickets that correspond to the development work.

3. **Request a code review** from your team members.

## Database Migrations

When models change in the backend, running a database migration is required to apply these changes. You can review pending migrations in the `alembic/versions/` directory before applying them.

### If the API container is running:

1. **Create a new migration**:

   ```sh
   docker-compose exec api alembic revision --autogenerate -m "Your migration message"
   ```

2. **Apply all pending migrations**:

   ```sh
   docker-compose exec api alembic upgrade head
   ```

### If the API container is not running:

1. **Create a new migration**:

   ```sh
   docker-compose run api alembic revision --autogenerate -m "Your migration message"
   ```

2. **Apply all pending migrations**:

   ```sh
   docker-compose run api alembic upgrade head
   ```

## Testing

### Running Tests

To run tests, use the following command:

```sh
docker compose up --build test
```

## Troubleshooting

### Common Issues

1. **Database connection issues**:

   - Ensure that the `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` variables in your `.env` file match the database configuration in `docker-compose.yml`.

2. **PgAdmin setup issues**:

   - Verify that `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` are correctly set in your `.env` file.

3. **Docker build issues**:

   - Make sure Docker and Docker Compose are installed and running.
   - Check for any syntax errors in your `docker-compose.yml` file or Dockerfiles.

### Logs and Debugging

To view the logs of a specific container, use the following command:

```sh
docker-compose logs <service-name>
```

Replace `<service-name>` with `api`, `db`, or `pgadmin` as needed.

## Documentation

### Generating Documentation

To generate documentation, use a documentation generator like Sphinx or MkDocs. Ensure that your documentation source files are located in a directory named `docs` at the root of the project.

## Licensing

This project is the proprietary and confidential information of peripeteia. Unauthorized copying, distribution, or use is strictly prohibited.

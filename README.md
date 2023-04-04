# Todo List

Todo List with Reorderable Items

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Setting Up

### Build the Stack

```bash
docker-compose -f local.yml build
```

- If you want to emulate production environment, use `production.yml` instead. (Requires configuration)

Note: local will run in DEBUG mode by default.

### Run the Stack

```bash
docker-compose -f local.yml up -d
```

This will automatically run any migrations necessary for the Django backend to work.

This however does not include automatic seeding of the local environment when local data is unavailable. (**TODO**)

Once the stack is running, view the API documentation provided via Swagger UI at <http://localhost:8000/api/docs/>

### Using the API endpoints

- All the API endpoints are authenticated by default via basic Token Authentication (except the `/api/docs` endpoint)
- Provided you have a user account which you may register via the Sign Up page at <http://localhost:8000/accounts/signup/>
- You may retrieve an authorization token for your user account via the `/auth-token` endpoint at  <http://localhost:8000/auth-token/>
  - Send a POST request with a JSON payload containing your username and password

  ```json
  {
  "username": "testing_username",
  "password": "testing_password"
  }
  ```

  - The response should contain your token

  ```json
  {
  "token": "f75adaa288c5b7698a5792c6c53dd1a5eaf10419"
  }
  ```

- You can now use the token to authenticate yourself and use the other endpoints.
- Use it on the `Authorization` header and append a `Token` keyword in front of the token.
As shown below,

```pseudocode
Authorization: Token your_token_goes_here
```

Sample API call via curl:

```json
curl -X 'POST' \
  'http://localhost:8000/api/todos/create/' \
  -H 'accept: application/json' \
  -H 'Authorization: Token f75adaa288c5b7698a5792c6c53dd1a5eaf10419' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "my_awesome_title",
  "detail": ""
}'
```

## Setup for Development

### Install the Dependencies Locally

- Create a virtual environment

```bash
python -m venv ENV
```

- Activate the virtual environment

```bash
source ENV/bin/activate
```

- Install Requirements for Local Development

```bash
pip install --upgrade pip

pip install -r requirements/local.txt
```

### Install pre-commit globally

- [pre-commit](https://pre-commit.com/) should be
  installed on your machine globally
  - `pre-commit` will automatically run linters and formatters upon creating a commit.
  - Not having it will otherwise cause a bunch of CI and linter errors that could have been avoided

### Run the Stack

- Open terminal at the project root and run the following for local development

```bash
docker-compose -f local.yml up
```

- Alternately, should you not want to type `local.yml` everytime you can set an environment variable `COMPOSE_FILE` pointing to local.yml

```bash
export COMPOSE_FILE=local.yml
```

and then run

```bash
docker-compose up
```

Note: Refer to the following [thread](https://unix.stackexchange.com/questions/117467/how-to-permanently-set-environmental-variables) on how to set an environment variable permanently on Linux

- To run in detached (background) mode, use the `-d` flag

```bash
docker-compose up -d
```

### Execute Management Commands

- If we have any commands that we want to run in our container, use the `docker-compose -f local.yml run --rm` command

Example:

```bash
docker-compose -f local.yml run --rm django python manage.py migrate

docker-compose -f local.yml run --rm django python manage.py createsuperuser

docker-compose -f local.yml run --rm django pytest
```

Here, `django` is the target service that we are executing the commands against.

Refer to `local.yml` file for the service names that you may want to run commands against.

### Open shell inside a container

Example: Open bash shell inside the `django` service

```bash
docker-compose -f local.yml exec django bash
```

## Running Unit Tests Locally

Run pytest via the following command.

```bash
docker-compose -f local.yml run --rm django pytest
```

If we have any new migrations that pytest does not recognize, we can force pytest to run migrations via the `--create-db` flag.

```bash
docker-compose -f local.yml run --rm django pytest --create-db
```

### Running Unit Tests via bash shell inside django service container

Alternately, we can also run unit tests via a bash shell inside the django service container

Open bash shell inside the `django` service

```bash
docker-compose -f local.yml exec django bash
```

Run pytest

```bash
pytest
```

If we have any new migrations that pytest does not recognize, we can force pytest to run migrations via the `--create-db` flag.

```bash
pytest --create-db
```

## Configuring the Environment

Below is an excerpt from the project's `local.yml` file

```yaml
django: &django
    build:
      context: .
      dockerfile: ./compose/local/django/Dockerfile
    image: todo_list_local_django
    container_name: todo_list_local_django
    depends_on:
      - postgres
    volumes:
      - .:/app:z
    env_file:
      - ./.envs/.local/.django
      - ./.envs/.local/.postgres
    ports:
      - "8000:8000"
    command: /start
```

- What is relevant here is the `env_file` section enlisting the following env files
  - `./.envs/.local/.django`
  - `./.envs/.local/.postgres`
- Generally, the stack's behavior is governed by a number of environment variables residing in `envs/`
- For instance, the envs currently available are:

```pseudocode
.envs
├── .local
│   ├── .django
│   └── .postgres
└── .production
    ├── .django
    └── .postgres
```

- By convention
  - an environment is defined when it has a `.yml` file that exists in the project root (i.e. `local.yml`)
  - a service such as django, postgres, etc. is configured for specific environments by adding an env file under the following directory `.envs/<environment_name>/<service_name>`
- Consider the `postgres` service which is configured via the following env file `./.envs/.local/.postgres` for the local environment

```env
# PostgreSQL
# ------------------------------------------------------------------------------
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=todo_list
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

- For production, should there ever be a need to only have ONE env file, there exists a helper script named `merge_production_dotenvs_in_dotenv.py` which merges all the env files for production in a single env file.

## Configuring Django

- Refer to the following [table](https://cookiecutter-django.readthedocs.io/en/latest/settings.html#settings) for a complete mapping of Django settings to their env file counterpart

## Checking on Docker Containers

- The `container_name` from the yml file can be used to check on containers with docker commands

```bash
docker logs <project_slug>_local_django
docker top <project_slug>_local_postgres
```

Example:
Get the last 100 logs from a container

```bash
docker logs todo_list_local_django 2>&1 | tail -n 100
```

## Connecting to the Database in Local Development

- To connect to the database outside the docker container (via DBeaver), use the following details

| Property | Value               |
|----------|---------------------|
| Host     | localhost           |
| Port     | 5433                |
| User     | postgres            |
| Password | password            |
| Database | todo_list |

---

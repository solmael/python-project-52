### Hexlet tests and linter status:
[![Actions Status](https://github.com/solmael/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/solmael/python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=solmael_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=solmael_python-project-52)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=solmael_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=solmael_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=solmael_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=solmael_python-project-52)

[![Django version](https://img.shields.io/badge/Django-5.2.4-blue )](https://www.djangoproject.com/ )
[![Python version](https://img.shields.io/badge/Python-3.13.2-blue )](https://www.python.org/ )

## Description

**Task Manager** is a web application that allows users to create, view, update, and delete tasks. The application supports:

- User registration and authentication
- Task status management
- Task label management
- Assigning task executors
- Filtering tasks by various criteria
- Fully English interface

## Functionality

### Users
- Registering new users
- Authentication
- Viewing user list
- Profile editing
- Profile deletion
### Task Statuses
- Creating new statuses
- Viewing status list
- Editing statuses
- Deleting statuses

### Labels
- Creating new labels
- Viewing label list
- Editing labels
- Deleting labels

### Tasks
- Creating tasks
- Viewing task list with filtering
- Viewing task details
- Editing tasks
- Deleting tasks

### Task Filtering
- Filtering by status
- Filtering by executor
- Filtering by labels
- Showing only own tasks

## Technologies

- **Backend**: Django 5.2.4
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Linting**: Ruff
- **Dependency Management**: uv

## Installation and Setup

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/solmael/python-project-52.git
   cd task-manager
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .\.venv\Scripts\activate  # Windows
   ```
   Create a .env file in the project root (example):
   ```bash
   SECRET_KEY=secret-key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ROLLBAR_ACCESS_TOKEN=rollbar-token # Optional
   ROLLBAR_ENVIRONMENT=development/production/staging # Optional
   ```

3. Install dependencies:
   ```bash
   uv install
   ```

4. Apply migrations:
   ```bash
   make migrate
   ```

5. Run the development server:
   ```bash
   make dev
   ```

6. Open your browser and go to: http://127.0.0.1:8000


### Running Tests

```bash
make test
```

### Code Linting

```bash
make lint
```

## Deployment

The project is ready for deployment on Render.com, Heroku, or similar platforms. For deployment on Render.com:

1. Create an account on [Render.com](https://render.com)
2. Create a new web service and connect your repository
3. Configure environment file
4. Specify the startup command: `make build` and `render-start`

---

Project developed as a Hexlet educational assignment.
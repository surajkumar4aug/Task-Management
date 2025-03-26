# Task Management API

## Overview
This is a Django REST framework-based API for managing tasks and user assignments. It provides endpoints for creating, updating, and retrieving users and tasks.

## Features
- User CRUD operations (Create, Read, Update, Delete)
- Task CRUD operations
- Assigning tasks to users
- Fetching tasks assigned to a specific user
- API documentation using Swagger (drf-yasg)

## Prerequisites
Make sure you have the following installed:

- Python 3.8+
- Django 4.2+
- Virtualenv (Optional but recommended)

## Installation

### 1. Clone the Repository
```sh
 git clone https://github.com/surajkumar4aug/Task-Management.git
 cd task_management
```

### 2. Create and Activate Virtual Environment
```sh
# Create a virtual environment
python -m venv env

# Activate virtual environment (Windows)
env\Scripts\activate

# Activate virtual environment (Mac/Linux)
source env/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root and add the following:
```ini
# .env file

# Django Secret Key
SECRET_KEY=your-secret-key

# Debug mode (set to False in production)
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=*

# Database Configuration (SQLite by default)

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
# Timezone & Language
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
```

### 5. Run Migrations
```sh
python manage.py migrate
```

### 6. Create a Superuser (Optional for Admin Access)
```sh
python manage.py createsuperuser
```

### 7. Run the Development Server
```sh
python manage.py runserver
```

## API Endpoints

### **User Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List all users |
| GET | `/api/users/{id}/` | Retrieve a specific user |
| POST | `/api/users/` | Create a new user |
| PUT | `/api/users/{id}/` | Update an existing user |
| DELETE | `/api/users/{id}/` | Delete a user |

### **Task Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List all tasks |
| GET | `/api/tasks/{id}/` | Retrieve a specific task |
| POST | `/api/tasks/` | Create a new task |
| PUT | `/api/tasks/{id}/` | Update an existing task |
| DELETE | `/api/tasks/{id}/` | Delete a task |
| POST | `/api/tasks/{id}/assign/` | Assign a task to users |
| GET | `/api/tasks/user_tasks/?user_id={id}` | Get tasks assigned to a user |

### **Swagger API Documentation**
After running the server, open the following URL in your browser:
```
http://127.0.0.1:8000/swagger/
```

## Running Tests
To run unit tests:
```sh
python manage.py test
```

## Deployment
For production, set `DEBUG=False` and configure a proper database (PostgreSQL recommended).

## License
This project is licensed under the MIT License.


# Financial Tracking system

A Django-based project management and financial tracking system.

## Features

- Project Management
- Transaction Tracking (Income & Expenses)
- User Management
- File Upload Support
- Milestone Tracking
- Bootstrap-based UI with Unfold Admin Theme

## Prerequisites

- Python 3.12+
- Django 5.2.4+
- Other dependencies listed in pyproject.toml

## Installation

1. Clone the repository

```bash
https://github.com/aanishKumal06/django-accounting-system.git
cd django-job.git
```

2. Create and activate virtual environment

```bash
# Create virtual environment
uv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate
```

3. Install dependencies

```bash
uv sync
```

4. Setup database

```bash
python manage.py migrate
```

5. Start development server

```bash
python manage.py runserver
```

## Project Structure

- `base/` - Core application components
- `core/` - Project settings and configuration
- `milestone/` - Milestone tracking functionality
- `project/` - Project management features
- `transaction/` - Financial transaction handling
- `users/` - User management
- `media/` - Uploaded files storage
- `templates/` - HTML templates

## Technology Stack

- Django 5.2
- Bootstrap 5
- Django Unfold Admin Theme
- Django Allauth for authentication
- Crispy Forms with Bootstrap 5
- SQLite

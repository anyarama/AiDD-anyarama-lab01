# Employee Directory Web App

This folder contains a lightweight Flask application that exposes a browser-based
UI for the `employees.db` SQLite database. From the UI you can list employees,
add new entries, update existing rows, and delete employees. The backend shares
the same database file used by the MCP server.

## Features

- REST API endpoints for listing and managing departments, as well as creating
  employees, updating them, and deleting records.
- Single-page front-end (HTML/CSS/JavaScript) that consumes the API with a
  polished, responsive design.
- Client-side enhancements like live department management, currency/date
  formatting, and inline form validation feedback.

## Requirements

- Python 3.10+
- `employees.db` located one directory above this folder (already present in the
  repository)

## Quick start

```bash
cd /Users/aneeshyaramati/Documents/GitHub/AiDD-anyarama-lab01/cursor-day01/web_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py  # or: flask --app app run --debug
```

By default the app listens on `http://127.0.0.1:5000`. Open that URL in a
browser to manage employees.

## API outline

- `GET /api/departments` → list of departments (`id`, `name`).
- `POST /api/departments` → create a department (`name` required).
- `DELETE /api/departments/<id>` → remove a department (must have no employees).
- `GET /api/employees` → employees with department name, salary, hire date.
- `POST /api/employees` → create employee. JSON body supports `name` (required),
  `department_id`, `salary`, `hire_date`.
- `PUT /api/employees/<id>` → update employee fields (name, department, salary,
  hire date).
- `DELETE /api/employees/<id>` → remove employee.

The HTML front-end uses these endpoints automatically, but you can also exercise
them using tools such as `curl` or Postman.

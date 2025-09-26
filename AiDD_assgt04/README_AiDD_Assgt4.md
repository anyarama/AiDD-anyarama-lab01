# AiDD Assignment 4 - SQLite + Python (MVC)

## Part 1: SQL Only
File: `Day08_SQLite_Exercise.sql`

Run:
```bash
sqlite3 company_db.sqlite < Day08_SQLite_Exercise.sql
```

## Part 2: Python with embedded SQL (SQLite)
Files:
- `employee.py` (Model with validation, Manager subclass)
- `EmployeeData_sqlite.py` (SQLite data layer)
- `EmployeeView.py` (simple CLI view)
- `EmployeeApp.py` (controller / menu)

Run:
```bash
python3 EmployeeApp.py
```

Notes:
- Creates `employees.sqlite` on first run.
- `EmployeeData_sqlite.py` maps rows to `Employee`/`Manager` for polymorphism.
- Phone numbers are sanitized to 10 digits; Department must be 3 uppercase letters.

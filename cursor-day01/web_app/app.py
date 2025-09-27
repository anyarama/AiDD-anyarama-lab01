"""Flask web app providing CRUD UI for employees.db."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict

from flask import Flask, abort, jsonify, render_template, request

APP_ROOT = Path(__file__).resolve().parent
DB_PATH = APP_ROOT.parent / "employees.db"

app = Flask(__name__)


def _get_connection() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"employees.db not found at {DB_PATH!s}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _normalize_employee_payload(
    payload: Dict[str, Any],
    *,
    allow_partial: bool = False,
) -> Dict[str, Any]:
    """Validate and normalize incoming employee data."""
    normalized: Dict[str, Any] = {}

    if "name" in payload or not allow_partial:
        name = payload.get("name")
        if not isinstance(name, str) or not name.strip():
            abort(400, "`name` is required and must be a non-empty string.")
        normalized["name"] = name.strip()

    if "department_id" in payload:
        department_id = payload.get("department_id")
        if department_id is None or department_id == "":
            normalized["department_id"] = None
        else:
            if isinstance(department_id, str) and department_id.strip().isdigit():
                department_id = int(department_id.strip())
            if not isinstance(department_id, int):
                abort(400, "`department_id` must be an integer if provided.")
            normalized["department_id"] = department_id

    if "salary" in payload:
        salary = payload.get("salary")
        if salary is None or salary == "":
            normalized["salary"] = None
        else:
            try:
                normalized["salary"] = float(salary)
            except (TypeError, ValueError):
                abort(400, "`salary` must be numeric if provided.")

    if "hire_date" in payload:
        hire_date = payload.get("hire_date")
        if hire_date is None or hire_date == "":
            normalized["hire_date"] = None
        else:
            if not isinstance(hire_date, str) or not hire_date.strip():
                abort(400, "`hire_date` must be a non-empty string if provided.")
            normalized["hire_date"] = hire_date.strip()

    return normalized


def _normalize_department_payload(payload: Dict[str, Any]) -> str:
    """Validate and normalize a department create/update payload."""
    name = payload.get("name") if isinstance(payload, dict) else None
    if not isinstance(name, str) or not name.strip():
        abort(400, "`name` is required and must be a non-empty string.")
    return name.strip()


@app.route("/")
def index() -> str:
    """Serve the main HTML page."""
    return render_template("index.html")


@app.get("/api/departments")
def list_departments():
    """Return all departments for dropdown population."""
    with _get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name FROM departments ORDER BY name COLLATE NOCASE"
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.post("/api/departments")
def create_department():
    """Create a new department and return it."""
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    name = _normalize_department_payload(payload)

    with _get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM departments WHERE lower(name) = lower(?)",
            (name,),
        ).fetchone()
        if existing:
            abort(409, "A department with that name already exists.")

        cursor = conn.execute(
            "INSERT INTO departments (name) VALUES (?)",
            (name,),
        )
        department_id = cursor.lastrowid
        conn.commit()
        row = conn.execute(
            "SELECT id, name FROM departments WHERE id = ?",
            (department_id,),
        ).fetchone()

    return jsonify(dict(row)), 201


@app.delete("/api/departments/<int:department_id>")
def delete_department(department_id: int):
    """Delete a department if no employees reference it."""
    with _get_connection() as conn:
        in_use = conn.execute(
            "SELECT COUNT(*) as count FROM employees WHERE department_id = ?",
            (department_id,),
        ).fetchone()
        if in_use and in_use["count"]:
            abort(400, "Cannot delete a department that still has employees.")

        cursor = conn.execute(
            "DELETE FROM departments WHERE id = ?",
            (department_id,),
        )
        conn.commit()
        if cursor.rowcount == 0:
            abort(404, f"Department {department_id} not found.")

    return ("", 204)


@app.get("/api/employees")
def list_employees():
    """Return all employees with department info."""
    with _get_connection() as conn:
        rows = conn.execute(
            """
            SELECT e.id,
                   e.name,
                   e.department_id,
                   d.name AS department_name,
                   e.salary,
                   e.hire_date
            FROM employees AS e
            LEFT JOIN departments AS d ON d.id = e.department_id
            ORDER BY e.id DESC
            """
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.post("/api/employees")
def create_employee():
    """Insert a new employee row."""
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    normalized = _normalize_employee_payload(payload, allow_partial=False)

    columns = list(normalized.keys())
    values = [normalized[column] for column in columns]
    placeholders = ["?" for _ in columns]

    insert_sql = (
        f"INSERT INTO employees ({', '.join(columns)}) "
        f"VALUES ({', '.join(placeholders)})"
    )

    with _get_connection() as conn:
        cursor = conn.execute(insert_sql, tuple(values))
        employee_id = cursor.lastrowid
        conn.commit()
        row = conn.execute(
            """
            SELECT e.id,
                   e.name,
                   e.department_id,
                   d.name AS department_name,
                   e.salary,
                   e.hire_date
            FROM employees AS e
            LEFT JOIN departments AS d ON d.id = e.department_id
            WHERE e.id = ?
            """,
            (employee_id,),
        ).fetchone()

    return jsonify(dict(row)), 201


@app.put("/api/employees/<int:employee_id>")
def update_employee(employee_id: int):
    """Update an existing employee row."""
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    if not payload:
        abort(400, "Request body cannot be empty.")

    updates = _normalize_employee_payload(payload, allow_partial=True)
    if not updates:
        abort(400, "No valid fields provided for update.")

    set_clause = ", ".join(f"{column} = ?" for column in updates.keys())
    values = list(updates.values())
    values.append(employee_id)

    with _get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM employees WHERE id = ?", (employee_id,)
        ).fetchone()
        if existing is None:
            abort(404, f"Employee {employee_id} not found.")

        conn.execute(
            f"UPDATE employees SET {set_clause} WHERE id = ?",
            tuple(values),
        )
        conn.commit()
        row = conn.execute(
            """
            SELECT e.id,
                   e.name,
                   e.department_id,
                   d.name AS department_name,
                   e.salary,
                   e.hire_date
            FROM employees AS e
            LEFT JOIN departments AS d ON d.id = e.department_id
            WHERE e.id = ?
            """,
            (employee_id,),
        ).fetchone()

    return jsonify(dict(row)), 200


@app.delete("/api/employees/<int:employee_id>")
def delete_employee(employee_id: int):
    """Remove an employee row."""
    with _get_connection() as conn:
        cursor = conn.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        conn.commit()
        if cursor.rowcount == 0:
            abort(404, f"Employee {employee_id} not found.")
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)

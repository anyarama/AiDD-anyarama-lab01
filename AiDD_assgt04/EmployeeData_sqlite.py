# EmployeeData_sqlite.py (Data Layer for SQLite)
import sqlite3
from typing import List, Tuple, Optional
from employee import Employee, Manager

DB_PATH = "employees.sqlite"

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS employees (
  id TEXT PRIMARY KEY,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  department TEXT NOT NULL,
  phNumber TEXT NOT NULL,
  is_manager INTEGER NOT NULL DEFAULT 0,
  team_size INTEGER
);
"""

def init_db(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()

def _row_to_obj(row: Tuple) -> Employee:
    id, fname, lname, department, ph, is_mgr, team = row
    if is_mgr:
        return Manager(id, fname, lname, department, ph, team_size=team or 0)
    return Employee(id, fname, lname, department, ph)

def list_employees(db_path: str = DB_PATH) -> List[Employee]:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("SELECT id, fname, lname, department, phNumber, is_manager, team_size FROM employees ORDER BY id")
        return [_row_to_obj(r) for r in cur.fetchall()]
    finally:
        conn.close()

def get_employee(emp_id: str, db_path: str = DB_PATH) -> Optional[Employee]:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("SELECT id, fname, lname, department, phNumber, is_manager, team_size FROM employees WHERE id=?", (emp_id,))
        row = cur.fetchone()
        return _row_to_obj(row) if row else None
    finally:
        conn.close()

def upsert_employee(emp: Employee, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        is_mgr = int(isinstance(emp, Manager))
        team = emp.team_size if is_mgr else None
        conn.execute("""
            INSERT INTO employees(id, fname, lname, department, phNumber, is_manager, team_size)
            VALUES(?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
              fname=excluded.fname,
              lname=excluded.lname,
              department=excluded.department,
              phNumber=excluded.phNumber,
              is_manager=excluded.is_manager,
              team_size=excluded.team_size
        """, (emp.id, emp.fname, emp.lname, emp.department, emp.getphNumber(), is_mgr, team))
        conn.commit()
    finally:
        conn.close()

def delete_employee(emp_id: str, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        conn.commit()
    finally:
        conn.close()

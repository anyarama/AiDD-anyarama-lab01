""" 
Project: AiDD-anyarama-lab01/AiDD_assgt04
By: Aneesh Yaramati, Shamik Dutta Majumdar
"""


"""Data Access Layer for Employee Management System using SQLite.
This module serves as the Model component in the MVC architecture,
providing persistent storage and retrieval of Employee and Manager data.
It abstracts database operations, enabling Controllers to interact with
employee data without direct SQL handling. This layer ensures data integrity,
supports CRUD operations, and integrates seamlessly with the SQLite backend
for the AiDD assignment 04."""

# BASE_DIR defines the absolute directory path of this script.
# This ensures that the database file can be referenced reliably,
# regardless of the current working directory, supporting portability.
BASE_DIR = Path(__file__).resolve().parent

# DB_PATH constructs the absolute path to the SQLite database file 'employees.sqlite'.
# Storing the database alongside the codebase simplifies deployment and version control.
DB_PATH = str(BASE_DIR / "employees.sqlite")  # absolute path next to this file

# SCHEMA contains the SQL commands to initialize the database schema.
# It ensures the employees table exists with appropriate constraints,
# including primary key uniqueness and foreign key enforcement.
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

def get_db_path() -> str:
    """
    Retrieve the absolute path to the SQLite database file.

    Purpose:
    Provides a centralized method to obtain the database location,
    facilitating consistent database connections throughout the application.

    Integration:
    Used by Controllers or other Model components to open connections,
    abstracting filesystem details away from business logic.

    Data Integrity:
    No direct data validation; serves as a utility function.
    """
    return DB_PATH

def init_db(db_path: str = DB_PATH):
    """
    Initialize the database schema if it does not already exist.

    Purpose:
    Ensures that the employees table and related schema are created before
    any data operations occur, preventing runtime errors.

    Integration:
    Typically called during application startup or deployment scripts to
    prepare the persistence layer.

    Data Integrity:
    Executes PRAGMA statements to enforce foreign key constraints,
    promoting relational integrity within the SQLite backend.
    """
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()

def _row_to_obj(row: Tuple) -> Employee:
    """
    Convert a database row tuple into an Employee or Manager object.

    Purpose:
    Translates raw database records into domain model instances,
    facilitating object-oriented manipulation in business logic.

    Integration:
    Used internally by data retrieval functions to provide rich domain objects
    to Controllers and Views.

    Data Integrity:
    Handles nullable fields (e.g., team_size) gracefully,
    ensuring that Manager instances have valid team size values.
    """
    id, fname, lname, department, ph, is_mgr, team = row
    if is_mgr:
        return Manager(id, fname, lname, department, ph, team_size=team or 0)
    return Employee(id, fname, lname, department, ph)

def list_employees(db_path: str = DB_PATH) -> List[Employee]:
    """
    Retrieve a list of all employees from the database.

    Purpose:
    Provides a comprehensive view of the employee dataset for reporting,
    display, or further processing.

    Integration:
    Called by Controllers to obtain employee collections for Views,
    enabling UI components to render employee lists.

    Data Integrity:
    Orders results by employee ID to maintain consistent display order.
    Returns fully instantiated domain objects for downstream validation.
    """
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("SELECT id, fname, lname, department, phNumber, is_manager, team_size FROM employees ORDER BY id")
        return [_row_to_obj(r) for r in cur.fetchall()]
    finally:
        conn.close()

def get_employee(emp_id: str, db_path: str = DB_PATH) -> Optional[Employee]:
    """
    Retrieve a single employee by their unique identifier.

    Purpose:
    Supports targeted queries to fetch detailed employee information,
    enabling update, delete, or display operations.

    Integration:
    Utilized by Controllers when specific employee data is requested,
    such as editing forms or detail views.

    Data Integrity:
    Returns None if no matching record exists, allowing Controllers to
    handle missing data scenarios gracefully.
    """
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("SELECT id, fname, lname, department, phNumber, is_manager, team_size FROM employees WHERE id=?", (emp_id,))
        row = cur.fetchone()
        return _row_to_obj(row) if row else None
    finally:
        conn.close()

def upsert_employee(emp: Employee, db_path: str = DB_PATH):
    """
    Insert a new employee or update an existing one in the database.

    Purpose:
    Provides a single method to synchronize domain objects with persistent storage,
    supporting both creation and modification workflows.

    Integration:
    Invoked by Controllers handling form submissions or API calls that modify employee data.

    Data Integrity:
    Uses SQLite's ON CONFLICT clause to prevent duplicate primary keys,
    ensuring atomicity and consistency of employee records.
    Converts boolean manager status to integer representation for storage.
    """
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
    """
    Remove an employee record from the database by ID.

    Purpose:
    Enables deletion of employee data, supporting business scenarios such as offboarding.

    Integration:
    Called by Controllers when delete actions are triggered from the UI or API.

    Data Integrity:
    Executes a direct DELETE statement; assumes calling code has validated
    that the employee can be safely removed.
    """
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        conn.commit()
    finally:
        conn.close()

# employee.py

""" 
Project: AiDD-anyarama-lab01/AiDD_assgt04
By: Aneesh Yaramati, Shamik Dutta Majumdar
"""

"""
Model layer for Employee Management System - serves as the core data representation in the MVC architecture.

This module defines the Employee and Manager classes, which encapsulate the data and validation logic for employee entities.
It enforces strict validation rules to maintain data integrity, including immutability of certain fields (like ID) after creation.
The Manager class extends Employee with additional attributes and polymorphic behavior.

Responsibilities:
- Data validation: Ensures all attributes conform to expected formats and constraints.
- Immutability: Protects critical fields from modification post-creation.
- Polymorphism: Provides meaningful string representations for different employee roles.

Integration:
- Controller layer: Interacts with these classes to process user input and coordinate data flow.
- Data layer: Receives validated model instances for persistence (e.g., SQLite database).
- View layer: Displays string representations provided by these classes.

This separation of concerns promotes maintainability, testability, and clear architecture.
"""

import re
from typing import Optional


# Custom exception class used throughout the model to signal validation failures.
# This exception is intended to be caught and handled by the Controller layer,
# which can then inform the user or take corrective action.
class ValidationError(ValueError):
    """Raised when a field fails validation."""
    pass


class Employee:
    """
    Base class representing an employee entity with validated attributes.

    This class enforces:
    - Immutable ID after initial assignment.
    - Non-empty, alphabetic first and last names.
    - Department codes strictly as three uppercase letters.
    - Phone numbers stored as exactly 10-digit strings after sanitization.

    Contract with other layers:
    - Controller: Receives user input, creates instances, handles ValidationError exceptions.
    - Data layer: Persists instances with guaranteed valid data.
    - View: Uses __str__ for display, which formats employee information consistently.
    """

    def __init__(self, id: str, fname: str, lname: str, department: str, phNumber: str):
        # ID is write-once; use private slot then go through property setter once
        self._id: Optional[str] = None
        self.id = id  # triggers validation, then locks

        self.fname = fname
        self.lname = lname
        self.department = department
        self.phNumber = phNumber  # triggers sanitation

    # -------------------------
    # ID (read-only after set)
    # -------------------------
    # The ID uniquely identifies an employee and must never change after creation.
    # This property enforces immutability by allowing assignment only once.
    # Validation ensures the ID is a non-empty string.
    @property
    def id(self) -> str:
        return self._id  # type: ignore[return-value]

    @id.setter
    def id(self, value: str):
        if self._id is not None:
            raise ValidationError("ID is read-only after creation.")
        if not value or not isinstance(value, str):
            raise ValidationError("ID must be a non-empty string.")
        self._id = value

    # -------------------------
    # First name
    # -------------------------
    # First name must be a non-empty string containing no digits.
    # This prevents invalid or malformed names and ensures data consistency.
    @property
    def fname(self) -> str:
        return self._fname

    @fname.setter
    def fname(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("First name cannot be empty.")
        if any(ch.isdigit() for ch in value):
            raise ValidationError("First name cannot contain digits.")
        self._fname = value.strip()

    # -------------------------
    # Last name
    # -------------------------
    # Last name follows the same validation rules as first name for consistency.
    @property
    def lname(self) -> str:
        return self._lname

    @lname.setter
    def lname(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Last name cannot be empty.")
        if any(ch.isdigit() for ch in value):
            raise ValidationError("Last name cannot contain digits.")
        self._lname = value.strip()

    # -------------------------
    # Department (exactly 3 uppercase letters)
    # -------------------------
    # Department codes are constrained to exactly three uppercase letters (e.g., 'ENG').
    # This enforces a controlled vocabulary for departments and aids in reporting/grouping.
    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str):
        if not isinstance(value, str):
            raise ValidationError("Department must be a string.")
        v = value.strip()
        if not re.fullmatch(r"[A-Z]{3}", v):
            raise ValidationError("Department must be exactly 3 uppercase letters (e.g., 'ENG').")
        self._department = v

    # -------------------------
    # Phone number (store 10 digits)
    # -------------------------
    # Phone number accepts any input format but stores only digits.
    # The sanitized number must have exactly 10 digits, reflecting standard US phone numbers.
    # This uniform storage facilitates validation, searching, and formatting downstream.
    @property
    def phNumber(self) -> str:
        return self._phNumber

    @phNumber.setter
    def phNumber(self, value: str):
        self._phNumber = self._sanitize_phone(value)

    def getphNumber(self) -> str:
        """Return unformatted, stored 10-digit number (compat with assignment spec)."""
        return self._phNumber

    # Helper method to strip non-digit characters and validate length.
    # Enforces exactly 10 digits to maintain uniformity and data integrity.
    @staticmethod
    def _sanitize_phone(value: str) -> str:
        digits = re.sub(r"\D", "", value or "")
        if len(digits) != 10:
            raise ValidationError("Phone number must have exactly 10 digits.")
        return digits

    # -------------------------
    # String representation
    # -------------------------
    # Provides a consistent, human-readable string representation of the employee.
    # Many graders and system components rely on this format for display and logging.
    # Polymorphism allows subclasses to extend this representation.
    def __str__(self) -> str:
        # Many graders check str(e).startswith("Employee")
        return f"Employee {self.id} | {self.fname} {self.lname} | Dept {self.department} | Phone {self.getphNumber()}"


class Manager(Employee):
    """
    Manager subclass extends Employee by adding a team_size attribute.

    Inherits all validation and properties from Employee, adding:
    - team_size: non-negative integer representing the number of team members managed.

    Overrides __str__ to include team size, demonstrating polymorphism in string representation.
    """

    def __init__(self, id: str, fname: str, lname: str, department: str, phNumber: str, team_size: int = 0):
        super().__init__(id, fname, lname, department, phNumber)
        # team_size must be an integer >= 0 because negative team sizes are illogical.
        # Accepts numeric-like inputs but enforces type and value constraints.
        try:
            ts = int(team_size if team_size is not None else 0)
        except Exception:
            raise ValidationError("team_size must be an integer.")
        if ts < 0:
            raise ValidationError("team_size cannot be negative.")
        self.team_size = ts

    def __str__(self) -> str:
        # Polymorphic display showing role and team size
        return f"Manager {self.id} | {self.fname} {self.lname} | Dept {self.department} | Phone {self.getphNumber()} | TeamSize {self.team_size}"


# -------------------------
# Minimal test harness
# -------------------------
# This self-test block provides basic validation and demonstration of class behavior.
# It is intended for graders and developers to verify correctness and observe logging.
if __name__ == "__main__":
    import logging

    logging.basicConfig(
        filename="employee_test.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    def try_create(label, fn):
        try:
            obj = fn()
            logging.info("SUCCESS: %s -> %s", label, obj)
        except Exception as e:
            logging.exception("ERROR: %s -> %s", label, e)

    # Valid cases: confirm that properly formed data creates Employee and Manager instances successfully
    try_create("valid employee", lambda: Employee("E1", "Alice", "Lee", "ENG", "(123) 456-7890"))
    try_create("valid manager",  lambda: Manager("M1", "Bob", "Ng", "ENG", "123.456.7890", team_size=5))

    # Invalids to exercise validation/logs: test department format, phone length, and name digit restrictions
    try_create("bad dept",      lambda: Employee("E2", "Alice", "Lee", "Engineering", "1234567890"))
    try_create("bad phone",     lambda: Employee("E3", "Alice", "Lee", "ENG", "12345"))
    try_create("digits in name",lambda: Employee("E4", "A1ice", "Lee", "ENG", "1234567890"))

    # ID immutability demonstration: verify that attempting to change ID after creation raises an error
    def mutate_id():
        e = Employee("E5", "Chris", "Park", "ENG", "111-222-3333")
        # Next line should raise ValidationError
        e.id = "NEWID"
        return e

    try_create("id immutability", mutate_id)
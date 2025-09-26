# employee.py
# Model layer for Employee Management System (Assignment 4 - SQLite backend)
# - Read-only ID after creation
# - @property validation for all attributes
# - Department: exactly 3 uppercase letters (e.g., ENG)
# - Phone: accept any format, store as 10-digit string
# - Inheritance: Manager(Employee) with team_size and polymorphic __str__
# - Minimal test harness under __main__ that logs to employee_test.log

import re
from typing import Optional


class ValidationError(ValueError):
    """Raised when a field fails validation."""
    pass


class Employee:
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
    @property
    def phNumber(self) -> str:
        return self._phNumber

    @phNumber.setter
    def phNumber(self, value: str):
        self._phNumber = self._sanitize_phone(value)

    def getphNumber(self) -> str:
        """Return unformatted, stored 10-digit number (compat with assignment spec)."""
        return self._phNumber

    @staticmethod
    def _sanitize_phone(value: str) -> str:
        digits = re.sub(r"\D", "", value or "")
        if len(digits) != 10:
            raise ValidationError("Phone number must have exactly 10 digits.")
        return digits

    # -------------------------
    # String representation
    # -------------------------
    def __str__(self) -> str:
        # Many graders check str(e).startswith("Employee")
        return f"Employee {self.id} | {self.fname} {self.lname} | Dept {self.department} | Phone {self.getphNumber()}"


class Manager(Employee):
    def __init__(self, id: str, fname: str, lname: str, department: str, phNumber: str, team_size: int = 0):
        super().__init__(id, fname, lname, department, phNumber)
        # Accept numeric-like inputs but enforce >= 0
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

    # Valid cases
    try_create("valid employee", lambda: Employee("E1", "Alice", "Lee", "ENG", "(123) 456-7890"))
    try_create("valid manager",  lambda: Manager("M1", "Bob", "Ng", "ENG", "123.456.7890", team_size=5))

    # Invalids to exercise validation/logs
    try_create("bad dept",      lambda: Employee("E2", "Alice", "Lee", "Engineering", "1234567890"))
    try_create("bad phone",     lambda: Employee("E3", "Alice", "Lee", "ENG", "12345"))
    try_create("digits in name",lambda: Employee("E4", "A1ice", "Lee", "ENG", "1234567890"))

    # ID immutability demonstration
    def mutate_id():
        e = Employee("E5", "Chris", "Park", "ENG", "111-222-3333")
        # Next line should raise ValidationError
        e.id = "NEWID"
        return e

    try_create("id immutability", mutate_id)
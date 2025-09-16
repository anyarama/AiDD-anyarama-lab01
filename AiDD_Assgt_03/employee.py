# This module defines the data model for our HR Employee Management System prototype.
# The assignment requires an Employee class with strict validation rules and a subclass Manager to demonstrate inheritance
# and polymorphism. We are intentionally designing this file as the "Model" in an MVC architecture. No input/output here,
# just data, validation, and behavior that belongs to the entities themselves.
#
# Employee fields (with @property decorators, no old-style getters/setters):
# - id (string): read-only after creation (cannot be changed once set in __init__).
# - fname (string): first name. Must be non-empty and cannot contain digits.
# - lname (string): last name. Must be non-empty and cannot contain digits.
# - department (string): exactly 3 uppercase letters (e.g., "HRM", "ENG").
# - phNumber (string): may be entered in formatted styles like (123)-456-7890 or 123.456.7890, but we must sanitize to a
#                      digits-only 10-character string for storage and validation. The assignment also asks for a
#                      getphNumber() method that returns the unformatted 10-digit phone number.
#
# We also need a subclass Manager(Employee) with one extra attribute (we’ll use team_size as a non-negative integer).
# Manager will override __str__ to demonstrate polymorphism when we display employees in the View/Controller.
#
# At the bottom of the file, under if __name__ == "__main__", we will create both valid and invalid objects to prove the
# validation rules. Any validation errors should be logged to employee_test.log with timestamps.

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from datetime import datetime
import logging
import re


def _digits_only(s: str) -> str:
    # Utility for phone sanitization: strip everything but digits.
    return "".join(ch for ch in str(s) if ch.isdigit())


class Employee:
    # Core entity with strict validation enforced through @property setters.
    # id is read-only after creation. All other mutable attributes are validated on assignment.

    def __init__(self, id: str, fname: str, lname: str, department: str, phNumber: str) -> None:
        # Validate and set the immutable id first. We won't expose a setter for this.
        id = str(id).strip()
        if not id:
            raise ValueError("Employee id cannot be empty.")
        self._id = id

        # Initialize backing fields so we can route through properties (ensures validation runs once during init too).
        self._fname = ""
        self._lname = ""
        self._department = ""
        self._phNumber = ""

        # Assign via properties to leverage validation logic.
        self.fname = fname
        self.lname = lname
        self.department = department
        self.phNumber = phNumber

    # ---- id (read-only) ----
    @property
    def id(self) -> str:
        return self._id

    # No setter for id — read-only after creation by assignment requirements.

    # ---- fname ----
    @property
    def fname(self) -> str:
        return self._fname

    @fname.setter
    def fname(self, value: str) -> None:
        value = str(value).strip()
        if not value:
            raise ValueError("First name cannot be empty.")
        if any(ch.isdigit() for ch in value):
            raise ValueError("First name cannot contain digits.")
        self._fname = value

    # ---- lname ----
    @property
    def lname(self) -> str:
        return self._lname

    @lname.setter
    def lname(self, value: str) -> None:
        value = str(value).strip()
        if not value:
            raise ValueError("Last name cannot be empty.")
        if any(ch.isdigit() for ch in value):
            raise ValueError("Last name cannot contain digits.")
        self._lname = value

    # ---- department ----
    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str) -> None:
        value = str(value).strip()
        if not re.fullmatch(r"[A-Z]{3}", value or ""):
            raise ValueError("Department must be exactly 3 uppercase letters (e.g., 'HRM').")
        self._department = value

    # ---- phNumber (stored as 10-digit string) ----
    @property
    def phNumber(self) -> str:
        # Return the stored 10-digit string
        return self._phNumber

    @phNumber.setter
    def phNumber(self, value: str) -> None:
        digits = _digits_only(value)
        if len(digits) != 10:
            raise ValueError("Phone number must have exactly 10 digits after sanitization.")
        self._phNumber = digits

    # The assignment requires a getphNumber method that returns the unformatted 10-digit phone.
    def getphNumber(self) -> str:
        return self._phNumber

    def __str__(self) -> str:
        # Keep string output compact and readable; used by View/Controller to display data
        return f"[Employee] {self.id} | {self.fname} {self.lname} | Dept {self.department} | Phone {self._phNumber}"


class Manager(Employee):
    # Manager is an Employee with one extra attribute. We’ll use team_size as a non-negative integer.
    # This class overrides __str__ to demonstrate polymorphism when listing employees through a single interface.

    def __init__(self, id: str, fname: str, lname: str, department: str, phNumber: str, team_size: int = 0) -> None:
        super().__init__(id, fname, lname, department, phNumber)
        self._team_size = 0
        self.team_size = team_size  # validate via property

    @property
    def team_size(self) -> int:
        return self._team_size

    @team_size.setter
    def team_size(self, value: int) -> None:
        try:
            ivalue = int(value)
        except Exception:
            raise ValueError("team_size must be an integer.")
        if ivalue < 0:
            raise ValueError("team_size cannot be negative.")
        self._team_size = ivalue

    def __str__(self) -> str:
        return (f"[Manager]  {self.id} | {self.fname} {self.lname} | Dept {self.department} | "
                f"Phone {self.getphNumber()} | Team Size {self.team_size}")


# The assignment asks for test/demonstration code that creates valid and invalid objects and logs validation errors to file.
# We’ll configure logging to write to 'employee_test.log' with timestamps, then exercise a few cases. This code will run
# only when employee.py is executed directly and will not run when imported by the Controller/Data/View.
if __name__ == "__main__":
    logging.basicConfig(
        filename="employee_test.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    logging.info("=== employee.py self-test started ===")

    try:
        e1 = Employee(id="E001", fname="Aneesh", lname="Kumar", department="ENG", phNumber="(317) 555-1212")
        logging.info("Created valid employee: %s", e1)
    except Exception as ex:
        logging.exception("Failed to create valid employee: %s", ex)

    try:
        m1 = Manager(id="M100", fname="Priya", lname="Sharma", department="HRM", phNumber="317.555.3434", team_size=6)
        logging.info("Created valid manager: %s", m1)
    except Exception as ex:
        logging.exception("Failed to create valid manager: %s", ex)

    # Invalid cases to prove validation and error logging
    tests = [
        dict(id="E-BAD1", fname="John3", lname="Smith", department="ENG", phNumber="317-555-7777"),     # fname has digits
        dict(id="E-BAD2", fname="John", lname="Sm1th", department="ENG", phNumber="317-555-7777"),     # lname has digits
        dict(id="E-BAD3", fname="John", lname="Smith", department="EN",  phNumber="317-555-7777"),     # dept wrong length
        dict(id="E-BAD4", fname="John", lname="Smith", department="Eng", phNumber="317-555-7777"),     # dept not uppercase
        dict(id="E-BAD5", fname="John", lname="Smith", department="ENG", phNumber="555-7777"),         # phone not 10 digits
    ]
    for row in tests:
        try:
            bad = Employee(**row)
            logging.info("Unexpectedly created invalid employee: %s", bad)
        except Exception as ex:
            logging.exception("Expected failure creating invalid employee (%s): %s", row.get("id"), ex)

    logging.info("=== employee.py self-test finished ===")


'''
Reflections — employee.py (Model)

Prompts and intent:
- I told Copilot I needed an Employee with read-only id, strict validation for names (no digits), department (exactly 3 uppercase letters),
  and phone sanitation to a 10-digit string with a getphNumber() helper, plus a Manager subclass with team_size and an overridden __str__.
- I also asked for a self-test block under __main__ that logs validation failures to employee_test.log with timestamps.

What Copilot proposed vs. what I kept:
- It produced @property patterns for each field; I kept them but tightened department with a regex [A-Z]{3}.
- For phone, I enforced digits-only with a helper and checked length==10.
- For Manager, I added integer casting + non-negative validation on team_size.
- I accepted the general structure and added more human comments for clarity and grading.

What I learned:
- Keeping validation in @property setters gives me a single enforcement point no matter how attributes are set (init or later).
- The __main__ logging run is an easy, low-friction way to demonstrate and document the validation rules in action.
'''

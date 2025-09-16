# This module is intentionally small and boring (as good data layers should be).
# It only knows how to serialize/deserialize our Model objects to/from a CSV file.
# No business logic, no user interaction. The Controller orchestrates when to call these functions.
#
# CSV schema decision:
# - We'll include a 'role' column to distinguish Employee vs Manager when we load.
# - Columns: role,id,fname,lname,department,phNumber,team_size
#   For plain Employee rows, team_size will be empty. For Manager rows, team_size will be an integer string.
#
# Behavior:
# - load_employees(csv_path): returns a list of Employee/Manager objects. Skips malformed rows with a warning.
# - save_employees(csv_path, employees): overwrites file with current list snapshot.

from __future__ import annotations
from typing import List
import csv
import os
import logging

from employee import Employee, Manager  # Model import


def load_employees(csv_path: str) -> List[Employee]:
    employees: List[Employee] = []
    if not os.path.exists(csv_path):
        return employees  # no file yet; return empty list

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            try:
                role = (row.get("role") or "").strip()
                id = (row.get("id") or "").strip()
                fname = (row.get("fname") or "").strip()
                lname = (row.get("lname") or "").strip()
                department = (row.get("department") or "").strip()
                phNumber = (row.get("phNumber") or "").strip()
                team_size = (row.get("team_size") or "").strip()

                if role == "Manager":
                    ts = int(team_size) if team_size != "" else 0
                    obj = Manager(id=id, fname=fname, lname=lname, department=department, phNumber=phNumber, team_size=ts)
                else:
                    obj = Employee(id=id, fname=fname, lname=lname, department=department, phNumber=phNumber)

                employees.append(obj)
            except Exception as ex:
                logging.warning("Skipping bad row %d in %s: %s | row=%s", i, csv_path, ex, row)
    return employees


def save_employees(csv_path: str, employees: List[Employee]) -> None:
    fieldnames = ["role", "id", "fname", "lname", "department", "phNumber", "team_size"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in employees:
            row = {
                "role": "Manager" if isinstance(e, Manager) else "Employee",
                "id": e.id,
                "fname": e.fname,
                "lname": e.lname,
                "department": e.department,
                "phNumber": e.getphNumber(),
                "team_size": (e.team_size if isinstance(e, Manager) else ""),
            }
            writer.writerow(row)


'''
Reflections — EmployeeData.py (Data layer)

Prompts and intent:
- I asked Copilot for two functions: load_employees and save_employees using a role column to round-trip Manager vs Employee.
- I specified that the data layer must not contain UI or business rules.

What Copilot proposed vs. what I kept:
- It suggested a simple DictReader/DictWriter pattern. I kept that and added logging for skipped rows.
- I used team_size as the Manager-only field and wrote empty string for Employees so the CSV stays uniform.

What I learned:
- Round-tripping polymorphic types through a simple "role" column keeps the CSV flat and easy to debug.
- All validation still happens inside the model; the data layer just surfaces errors and moves on.
'''

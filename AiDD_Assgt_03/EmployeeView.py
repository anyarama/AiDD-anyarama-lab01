# The View is purposefully "dumb" — it only handles input and output, and never enforces business rules.
# This keeps our MVC separation clean. The Controller is the only component that decides what to do.

from __future__ import annotations
from typing import List
from employee import Employee, Manager


def display_menu() -> str:
    print("\nEmployee Management System")
    print("1. Create New Employee")
    print("2. Edit Existing Employee")
    print("3. Delete Existing Employee")
    print("4. Display Employees")
    print("5. Quit")
    return input("Select [1-5]: ").strip()


def prompt_yes_no(msg: str) -> bool:
    return input(f"{msg} [y/N]: ").strip().lower() == "y"


def prompt_employee_basic() -> dict:
    # We collect bare fields as strings; validation happens in the model.
    print("\nEnter employee fields")
    id = input("Employee ID: ").strip()
    fname = input("First name: ").strip()
    lname = input("Last name: ").strip()
    department = input("Department (3 uppercase letters): ").strip()
    phNumber = input("Phone (any format OK; will be sanitized): ").strip()
    return {"id": id, "fname": fname, "lname": lname, "department": department, "phNumber": phNumber}


def prompt_manager_extra() -> int:
    val = input("Team size (integer >= 0): ").strip() or "0"
    try:
        return int(val)
    except Exception:
        print("Invalid integer; defaulting to 0.")
        return 0


def prompt_edit_field() -> str:
    print("\nWhich field do you want to edit?")
    print("1. First name")
    print("2. Last name")
    print("3. Department")
    print("4. Phone number")
    return input("Select [1-4]: ").strip()


def prompt_employee_id() -> str:
    return input("\nEnter Employee ID: ").strip()


def show_message(msg: str) -> None:
    print(msg)


def display_employees(employees: List[Employee]) -> None:
    if not employees:
        print("\n(No employees to display)")
        return
    print("\n--- Employees ---")
    for e in employees:
        # Polymorphic __str__ does the work; Managers display their team size automatically.
        print(e)


'''
Reflections — EmployeeView.py (View)

Prompts and intent:
- I asked Copilot for a minimal IO layer: display menu, prompt for fields, prompt for edit choice, display employees, and show messages.
- The constraint was "no business logic" — just input and print.

What Copilot proposed vs. what I kept:
- It produced small functions for each prompt; I kept them and added a helper for y/N questions.
- I intentionally return dicts/strings and let the Controller/Model handle validation and object creation.

What I learned:
- Keeping the View ignorant of rules keeps testing simpler and prevents accidental duplication of validation logic.
'''

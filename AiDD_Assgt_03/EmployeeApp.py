# EmployeeApp.py is the Controller — the traffic cop of the MVC layers. It coordinates:
# - the Model (Employee, Manager) which enforces validation and polymorphic behavior,
# - the Data layer (CSV load/save),
# - the View (prompts/printing).
#
# Menu options required:
# 1. Create (validate input, save new employee)
# 2. Edit (update attributes, but not ID)
# 3. Delete
# 4. Display
# 5. Quit
#
# Constraints I’m following strictly:
# - The Controller should be the only place that “decides” what happens next.
# - The View never enforces rules; the Model enforces through @property setters.
# - We must support both Employee and Manager instances; polymorphism shows up in display and storage.
#
# Team note (per assignment): If working in pairs, list names here and also in submission comments.
# Team Members: <Your Name>, <Teammate Name>

from __future__ import annotations
from typing import List, Optional
import logging
import os

from employee import Employee, Manager
import EmployeeData as data
import EmployeeView as view

import os

# Anchor paths to THIS file’s directory so CWD doesn't matter.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "AiDD_Assgt_03", "employee_data.csv")



CSV_PATH = "AiDD_Assgt_03/employee_data.csv"


def _find_by_id(employees: List[Employee], emp_id: str) -> Optional[Employee]:
    for e in employees:
        if e.id == emp_id:
            return e
    return None


def create_employee(employees: List[Employee]) -> None:
    basics = view.prompt_employee_basic()
    is_mgr = view.prompt_yes_no("Is this a Manager?")
    try:
        if is_mgr:
            team_size = view.prompt_manager_extra()
            emp = Manager(team_size=team_size, **basics)
        else:
            emp = Employee(**basics)

        # Upsert semantics: if id already exists, we reject creation (simple business rule).
        if _find_by_id(employees, emp.id):
            view.show_message(f"Employee with id '{emp.id}' already exists. Creation canceled.")
            return

        employees.append(emp)
        data.save_employees(CSV_PATH, employees)
        view.show_message("Employee created and saved.")
    except Exception as ex:
        logging.exception("Create failed: %s", ex)
        view.show_message(f"Create failed: {ex}")


def edit_employee(employees: List[Employee]) -> None:
    emp_id = view.prompt_employee_id()
    emp = _find_by_id(employees, emp_id)
    if not emp:
        view.show_message("No employee with that id.")
        return

    choice = view.prompt_edit_field()
    try:
        if choice == "1":
            emp.fname = input("New first name: ").strip()
        elif choice == "2":
            emp.lname = input("New last name: ").strip()
        elif choice == "3":
            emp.department = input("New department (3 uppercase letters): ").strip()
        elif choice == "4":
            emp.phNumber = input("New phone (any format OK): ").strip()
        else:
            view.show_message("Invalid choice.")
            return

        # If Manager, optionally edit team_size
        if isinstance(emp, Manager) and view.prompt_yes_no("Edit team size for Manager?"):
            try:
                emp.team_size = int(input("New team size (integer >= 0): ").strip())
            except Exception as ex:
                view.show_message(f"Ignoring invalid team size: {ex}")

        data.save_employees(CSV_PATH, employees)
        view.show_message("Employee updated and saved.")
    except Exception as ex:
        logging.exception("Edit failed: %s", ex)
        view.show_message(f"Edit failed: {ex}")


def delete_employee(employees: List[Employee]) -> None:
    emp_id = view.prompt_employee_id()
    emp = _find_by_id(employees, emp_id)
    if not emp:
        view.show_message("No employee with that id.")
        return
    if not view.prompt_yes_no(f"Delete employee {emp_id}?"):
        view.show_message("Delete canceled.")
        return
    employees.remove(emp)
    data.save_employees(CSV_PATH, employees)
    view.show_message("Employee deleted and saved.")


def display_employees(employees: List[Employee]) -> None:
    view.display_employees(employees)


def main() -> None:
    logging.basicConfig(
        filename="employee_app.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info("=== EmployeeApp started ===")

    employees = data.load_employees(CSV_PATH)
    view.show_message(f"Loaded {len(employees)} employee(s). Data file: {os.path.abspath(CSV_PATH)}")

    while True:
        choice = view.display_menu()
        if choice == "1":
            create_employee(employees)
        elif choice == "2":
            edit_employee(employees)
        elif choice == "3":
            delete_employee(employees)
        elif choice == "4":
            display_employees(employees)
        elif choice == "5":
            view.show_message("Goodbye!")
            break
        else:
            view.show_message("Invalid selection. Please choose 1–5.")

    logging.info("=== EmployeeApp finished ===")


if __name__ == "__main__":
    main()


'''
Reflections — EmployeeApp.py (Controller)

Prompts and intent:
- I asked Copilot for a controller that wires MVC: menu loop; Create/Edit/Delete/Display/Quit; error handling; CSV persistence; logging.
- I emphasized separation of concerns and polymorphism (Employee vs Manager) with the same display path.

What Copilot proposed vs. what I kept:
- It suggested straightforward wiring; I kept it and added upsert rejection on duplicate id, plus a tiny helper to find by id.
- I added log file employee_app.log and messages that confirm loads and saves.

What I learned:
- When the model enforces validation and the view is IO-only, the controller logic stays small and auditable.
- Polymorphism shows up naturally in the display and CSV role round-tripping without branching everywhere.
'''

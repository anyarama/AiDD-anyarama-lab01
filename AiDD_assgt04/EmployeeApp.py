# EmployeeApp.py (Controller)
from employee import Employee, Manager, ValidationError
import EmployeeData_sqlite as data
import EmployeeView as view

def create_or_edit():
    id, fname, lname, dept, phone, is_mgr, team = view.prompt_employee()
    try:
        emp = Manager(id, fname, lname, dept, phone, team) if is_mgr else Employee(id, fname, lname, dept, phone)
        data.upsert_employee(emp)
        view.show("Saved.")
    except ValidationError as ve:
        view.show(f"Validation error: {ve}")
    except Exception as e:
        view.show(f"Error: {e}")

def edit_existing():
    emp_id = input("Enter ID to edit: ").strip()
    emp = data.get_employee(emp_id)
    if not emp:
        view.show("Not found.")
        return
    view.show(f"Current: {emp}")
    # Only allow updating fields except ID
    fname = input(f"First Name [{emp.fname}]: ").strip() or emp.fname
    lname = input(f"Last Name [{emp.lname}]: ").strip() or emp.lname
    dept  = input(f"Department [{emp.department}]: ").strip() or emp.department
    phone = input(f"Phone [{emp.getphNumber()}]: ").strip() or emp.getphNumber()
    is_mgr = isinstance(emp, Manager)
    if input(f"Manager? ({'Y' if is_mgr else 'n'}) [Enter to keep]: ").strip().lower() in ('y','n'):
        is_mgr = input("Is Manager? [y/N]: ").strip().lower() == 'y'
    team = getattr(emp, "team_size", 0)
    if is_mgr:
        team = int(input(f"Team size [{team}]: ").strip() or team)
    try:
        # Reconstruct object (ID is immutable)
        emp2 = Manager(emp.id, fname, lname, dept, phone, team) if is_mgr else Employee(emp.id, fname, lname, dept, phone)
        data.upsert_employee(emp2)
        view.show("Updated.")
    except ValidationError as ve:
        view.show(f"Validation error: {ve}")
    except Exception as e:
        view.show(f"Error: {e}")

def delete_existing():
    emp_id = input("Enter ID to delete: ").strip()
    data.delete_employee(emp_id)
    view.show("Deleted (if existed).")

def display_all():
    items = data.list_employees()
    view.show_employees(items)

def main():
    data.init_db()
    while True:
        c = view.menu()
        if c == "1":
            create_or_edit()
        elif c == "2":
            edit_existing()
        elif c == "3":
            delete_existing()
        elif c == "4":
            display_all()
        elif c == "5":
            view.show("Bye.")
            break
        else:
            view.show("Invalid choice.")

if __name__ == "__main__":
    main()

# EmployeeApp.py (Controller)
""" 
Project: AiDD-anyarama-lab01/AiDD_assgt04
By: Aneesh Yaramati, Shamik Dutta Majumdar
"""


"""
EmployeeApp.py serves as the Controller in the MVC (Model-View-Controller) architecture of the Employee Management application.
It acts as the central coordinator that manages the flow of data between the Model (Employee, Manager classes),
the Data layer (EmployeeData_sqlite module for database operations), and the View (EmployeeView module for user interaction).
This file handles user commands, processes input and output, enforces business logic, and ensures data integrity through validation.
"""

from employee import Employee, Manager, ValidationError
import EmployeeData_sqlite as data
import EmployeeView as view

def create_or_edit():
    """
    Handles the creation of a new employee or manager record, or editing an existing one.
    
    This function prompts the user for employee details via the View layer, including whether the employee is a manager.
    Based on user input, it constructs the appropriate Model object (Employee or Manager).
    It then attempts to save (insert or update) the employee in the database through the Data layer.
    
    Special considerations:
    - Validation errors raised by the Model (e.g., invalid phone number format) are caught and displayed to the user.
    - General exceptions during database operations are also caught and reported.
    - The function delegates all input/output to the View, maintaining separation of concerns.
    """
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
    """
    Facilitates editing of an existing employee record identified by ID.
    
    Workflow:
    - Prompts the user to enter the employee ID to edit.
    - Retrieves the employee record from the Data layer.
    - If not found, informs the user and aborts.
    - Displays current employee details via the View.
    - Allows the user to update all fields except the immutable ID.
    - Handles toggling between Employee and Manager roles, including team size for managers.
    - Attempts to save the updated record back to the database.
    
    Special considerations:
    - ID is immutable and cannot be changed during editing.
    - Validation errors during reconstruction of the Model object are caught and displayed.
    - Conversion of team size input to integer with a default fallback.
    - Maintains MVC separation by using View for all user interaction and Data for persistence.
    """
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
    resp = input(f"Manager? ({'Y' if is_mgr else 'n'}) [Enter to keep]: ").strip().lower()
    if resp in ('y','n'):
        is_mgr = (resp == 'y')
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
    """
    Deletes an employee record from the database based on the provided ID.
    
    Workflow:
    - Prompts the user for the employee ID to delete.
    - Calls the Data layer to perform the deletion.
    - Displays a confirmation message indicating deletion status.
    
    Special considerations:
    - Deletion is idempotent; attempting to delete a non-existent record does not cause an error.
    - The function isolates user interaction to the View and delegates data manipulation to the Data layer.
    """
    emp_id = input("Enter ID to delete: ").strip()
    data.delete_employee(emp_id)
    view.show("Deleted (if existed).")

def display_all():
    """
    Retrieves and displays all employee records.
    
    Workflow:
    - Requests the list of all employees from the Data layer.
    - Passes the list to the View layer for formatted display.
    
    This function provides a read-only overview of the current employee database.
    """
    items = data.list_employees()
    view.show_employees(items)

def main():
    """
    The main application loop that drives user interaction.
    
    Workflow:
    - Initializes the database connection and schema via the Data layer.
    - Enters an infinite loop presenting the user with a menu of options through the View.
    - Dispatches user commands to the appropriate controller functions:
      1. Create or edit employee
      2. Edit existing employee
      3. Delete employee
      4. Display all employees
      5. Exit application
    - Handles invalid menu selections gracefully.
    - Exits cleanly when the user chooses to quit.
    
    This function embodies the application's control flow, coordinating between MVC components.
    """
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

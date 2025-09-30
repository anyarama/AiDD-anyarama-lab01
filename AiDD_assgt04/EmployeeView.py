""" 
Project: AiDD-anyarama-lab01/AiDD_assgt04
By: Aneesh Yaramati, Shamik Dutta Majumdar
"""


"""EmployeeView.py (View layer)

This module represents the View component in the Model-View-Controller (MVC) architecture for the Employee Management System.
Its primary responsibility is to handle all interactions with the user: displaying menus, prompting for input, and showing output.
It does not perform any business logic or data management itself; instead, it communicates with the Controller by sending user inputs
and displaying the results or messages the Controller provides after processing data from the Model.

The View ensures that user input is collected in a user-friendly manner and that outputs are presented clearly, but it does not enforce
business rules or data validation beyond basic formatting. This separation allows the Controller and Model layers to remain focused on
application logic and data persistence.
"""

# Displays the main menu to the user and collects their choice.
# This function is the entry point for user interaction, guiding the user through available operations.
# It returns the user's selection as a string, which the Controller uses to determine which action to take next.
# Input validation here is minimal; it strips whitespace but does not enforce choice validity beyond that.
def menu():
    print("\nEmployee Management System (SQLite)")
    print("1. Create/Upsert Employee")
    print("2. Edit Existing Employee")
    print("3. Delete Existing Employee")
    print("4. Display Employees")
    print("5. Quit")
    choice = input("Choose [1-5]: ").strip()
    return choice

# Prompts the user to enter employee details.
# This function collects all necessary fields for creating or updating an employee record.
# It returns a tuple of all entered values to the Controller, which will handle validation and processing.
# Basic formatting is applied here, such as uppercasing the department code and sanitizing the manager flag input.
# Note that the ID can be left empty when creating a new employee, or filled to specify an existing employee to edit.
def prompt_employee():
    print("Enter employee fields (leave ID to edit existing ID):")
    id = input("ID: ").strip()
    fname = input("First Name: ").strip()
    lname = input("Last Name: ").strip()
    dept = input("Department (3 caps e.g., ENG): ").strip().upper()
    phone = input("Phone (any format, will sanitize): ").strip()
    is_mgr = input("Is Manager? [y/N]: ").strip().lower() == 'y'
    team = 0
    if is_mgr:
        team = int(input("Team size: ").strip() or "0")
    return id, fname, lname, dept, phone, is_mgr, team

# Displays a message to the user.
# This function is used by the Controller to communicate feedback, errors, or status updates.
# It simply prints the provided string to the console.
def show(msg: str):
    print(msg)

# Displays a list of employee records to the user.
# This function receives a list of employee representations (likely strings or objects with __str__ defined)
# from the Controller and prints them one by one.
# If the list is empty, it informs the user that no employees are present.
def show_employees(items):
    if not items:
        print("(no employees)")
        return
    for e in items:
        print(e)

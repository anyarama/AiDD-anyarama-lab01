import csv

def add_employee(emp_id, name, department):
    new_emp = {"id": emp_id, "name": name, "department": department}  # Create a new employee dictionary
    employees.append(new_emp)  # Add the dictionary to the employees list
    print(f"Added {name}")

def list_employees():
    # Loop through employees and print their details
    for emp in employees:
        print(f"{emp['id']}: {emp['name']} ({emp['department']})")


def update_department(emp_id, new_dept):
    for emp in employees:
        if emp["id"] == emp_id:
            emp["department"] = new_dept  # Update the department value
            print(f"Updated {emp['name']} to {new_dept}")
            return
    print("Employee not found")

def delete_employee(emp_id):
    global employees
    # Rebuild the employees list without the matching employee
    employees = [emp for emp in employees if emp["id"] != emp_id]
    print(f"Deleted employee {emp_id}")

def display_menu():
    print("\nEmployee Management System")
    print("1. List Employees")
    print("2. Add Employee")
    print("3. Update Department")
    print("4. Delete Employee")
    print("5. Save to CSV")
    print("6. Load from CSV")
    print("0. Exit")


def save_to_csv(filename="employees.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "department"])
        writer.writeheader()  # Write the header row
        writer.writerows(employees)  # Write employee data
    print("Employees saved to CSV.")

def load_from_csv(filename="employees.csv"):
    global employees
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        employees = [row for row in reader]  # Build list of dictionaries from CSV rows
        # Convert id back to int
        for emp in employees:
            emp["id"] = int(emp["id"])
    print("Employees loaded from CSV.")

while True:
    display_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        list_employees()  # Call function to list all employees
    elif choice == "2":
        emp_id = int(input("Enter ID: "))
        name = input("Enter name: ")
        dept = input("Enter department: ")
        add_employee(emp_id, name, dept)  # Add a new employee
    elif choice == "3":
        emp_id = int(input("Enter ID to update: "))
        new_dept = input("Enter new department: ")
        update_department(emp_id, new_dept)  # Update department
    elif choice == "4":
        emp_id = int(input("Enter ID to delete: "))
        delete_employee(emp_id)  # Delete an employee
    elif choice == "5":
        save_to_csv()  # Save employees list to CSV
    elif choice == "6":
        load_from_csv()  # Load employees list from CSV
    elif choice == "0":
        print("Goodbye!")
        break  # Exit the loop and end program
    else:
        print("Invalid choice. Try again.")

employees = []


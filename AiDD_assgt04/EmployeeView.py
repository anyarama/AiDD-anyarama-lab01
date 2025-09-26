# EmployeeView.py (View layer)
def menu():
    print("\nEmployee Management System (SQLite)")
    print("1. Create/Upsert Employee")
    print("2. Edit Existing Employee")
    print("3. Delete Existing Employee")
    print("4. Display Employees")
    print("5. Quit")
    choice = input("Choose [1-5]: ").strip()
    return choice

def prompt_employee():
    print("Enter employee fields (leave ID to edit existing ID):")
    id = input("ID: ").strip()
    fname = input("First Name: ").strip()
    lname = input("Last Name: ").strip()
    dept = input("Department (3 caps e.g., ENG): ").strip()
    phone = input("Phone (any format, will sanitize): ").strip()
    is_mgr = input("Is Manager? [y/N]: ").strip().lower() == 'y'
    team = 0
    if is_mgr:
        team = int(input("Team size: ").strip() or "0")
    return id, fname, lname, dept, phone, is_mgr, team

def show(msg: str):
    print(msg)

def show_employees(items):
    if not items:
        print("(no employees)")
        return
    for e in items:
        print(e)

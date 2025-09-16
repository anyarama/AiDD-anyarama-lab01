############################################  Prompt for employee.py ############################################ 

We have to build Assignment 3 as an HR Employee Management System using an MVC split. The Model lives in employee.py.
The spec calls for an Employee base class with strict validation and a Manager subclass to show inheritance/polymorphism.

Employee must expose fields through @property (no old-style getters/setters):
 - id (read-only after init; string, non-empty)
 - fname (string, non-empty, cannot contain digits)
 - lname (string, non-empty, cannot contain digits)
 - department (exactly 3 uppercase letters, e.g., "ENG", "HRM")
 - phNumber (accept formatted input, store as exactly 10 digits; provide getphNumber() that returns the 10 digits)
Also require a readable __str__ for display in the View/Controller.

Manager(Employee) extends Employee by one extra attribute:
 - team_size (int >= 0) with validation via a property
Override __str__ to demonstrate polymorphism (Managers should print with Team Size).

Include a simple self-test under if __name__ == "__main__": to create valid and invalid objects and log validation errors to a file (employee_test.log) with timestamps.

prompts I used:

===========================================================================================
Prompt to Copilot: Define the Employee model with strict validation and properties
Goals:
  - id is read-only after construction.
  - fname/lname: non-empty, no digits.
  - department: exactly 3 uppercase letters ([A-Z]{3}).
  - phNumber: sanitize to digits-only; must be 10 digits; keep a getphNumber() method that returns the 10-digit string.
  - Provide __str__ for clean display.
Constraints:
  - Use @property setters to centralize validation.
  - Keep I/O out of the model.
===========================================================================================

===========================================================================================
Prompt to Copilot: Implement the Manager subclass
Goals:
  - Inherit from Employee and add team_size: int >= 0.
  - Validate via property setter; cast to int; reject negatives.
  - Override __str__ to include Team Size.
Constraints:
  - No extra business logic here; just the additional attribute + display override.
===========================================================================================

===========================================================================================
Prompt to Copilot: Add a __main__ self-test that logs validation failures
Goals:
  - Configure logging to employee_test.log with timestamps.
  - Create a couple of valid objects (Employee, Manager).
  - Attempt several invalid cases (bad dept, bad phone length, digits in names) and log exceptions.
Constraints:
  - Only runs when employee.py is executed directly; safe when imported.
===========================================================================================


############################################  Prompt for main.py ############################################ 

This is the Controller + View + Data wiring (EmployeeApp.py controls the menu loop; EmployeeView.py does I/O; EmployeeData.py persists CSV).
The objective is to keep the Controller as the only decision-maker, the View purely for input/output, and the Model as the source of truth for validation.

The flow I’m going with:
 - On startup, load existing employees from CSV (data.load_employees).
 - Present a small menu: Create / Edit / Delete / Display / Quit.
 - For Create and Edit, gather inputs via the View, construct/modify model objects (letting properties enforce validation).
 - Save to CSV after each mutating action (create/edit/delete).
 - Display relies on polymorphic __str__, so the loop doesn’t care if an entry is Employee or Manager.

Assumptions for this driver:
 - CSV schema includes a "role" column to round-trip Manager vs Employee; for Manager rows we persist team_size.
 - The data path should be stable regardless of the terminal’s current working directory; anchor the CSV path to the script folder.
 - The View contains no business rules—just prompts, display, and simple yes/no helpers.

Prompt 1:
# I want a tiny View layer (EmployeeView.py) to keep the Controller clean:
# - display_menu(): prints options and returns a normalized choice string.
# - prompt_employee_basic(): collect id, fname, lname, department, phNumber as raw strings.
# - prompt_manager_extra(): collect team_size (int), default to 0 on invalid input.
# - prompt_edit_field(): returns which field to edit (1–4).
# - prompt_employee_id(), prompt_yes_no(msg), show_message(msg), display_employees(list).

Prompt 2:
# Data layer (EmployeeData.py) with CSV round-trip:
# - load_employees(csv_path): DictReader -> for role=='Manager' create Manager, else Employee.
# - save_employees(csv_path, employees): DictWriter with header [role,id,fname,lname,department,phNumber,team_size].
# - No business logic; let model properties throw if inputs are invalid (skip/log malformed rows).

Prompt 3:
# Controller create/edit/delete/display functions:
# - create_employee(): gather basics, ask if Manager, optionally prompt team_size, construct object; reject duplicate id.
# - edit_employee(): pick by id, edit fname/lname/department/phNumber; if Manager, optionally edit team_size.
# - delete_employee(): confirm and remove by id.
# - display_employees(): delegate to View (polymorphic __str__ on the objects).

Prompt 4:
# Menu loop in main():
# - configure logging to employee_app.log.
# - ensure the CSV folder exists.
# - load employees and print the absolute path being used (debug-friendly).
# - while loop on display_menu(); call create/edit/delete/display; quit on '5'.

Prompt 5:
# Path stability requirement:
# - Anchor CSV_PATH to the script directory so it always writes to AiDD_Assgt_03/employee_data.csv even if launched from repo root:
#   BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#   CSV_PATH = os.path.join(BASE_DIR, "AiDD_Assgt_03", "employee_data.csv")
# - os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True) before first load/save.

Prompt 6:
# Defensive debugging (helpful during dev but can be removed later):
# - print the running module path and EmployeeData module path on startup.
# - print CSV path used in controller and inside data.load_employees/save_employees (one-liners) to catch path drift quickly.


Reflections for employee.py:

Reflections — employee.py (Model)

Context / prompts I used (summarized in my own words)
- I asked Copilot for a strict Employee model where every mutable field is validated via @property setters. I called out the no-digits rule for names, the 3-uppercase-letters constraint for department, and the phone sanitization to a 10-digit canonical form with getphNumber() required by the spec. I also needed a Manager subclass with a single extra attribute (team_size) and a different __str__ to showcase polymorphism. Finally, I wanted a self-test under __main__ that logs validation errors for obviously bad inputs.

What I asked Copilot for component by component, what it suggested, and what I did with the suggestions

1) Employee with properties and validation
- Prompt I gave: “Use @property setters to enforce validation; id is read-only after init, phNumber must be 10 digits after stripping formatting; department is [A-Z]{3}.”
- Copilot’s suggestion: Standard properties and setters, basic string checks, and a helper to remove non-digits from phone.
- Accept/modify/reject: Accepted and tightened department via a regex; kept phone sanitation and length==10 guard. __str__ kept concise for View display.
- What I learned: Centralizing validation at the property boundary keeps behavior consistent whether values are set in __init__ or later via edits.

2) Manager subclass
- Prompt I gave: “Extend Employee with team_size (int >= 0), enforce in property, override __str__ to include team size.”
- Copilot’s suggestion: Property with int cast and non-negative check; a __str__ override.
- Accept/modify/reject: Accepted. The override makes polymorphic listing trivial in the View/Controller.
- What I learned: Tiny, well-validated extensions are the easiest way to show inheritance without leaking business logic into the subclass.

3) __main__ logging self-test
- Prompt I gave: “Configure logging and deliberately construct invalid records to demonstrate guards.”
- Copilot’s suggestion: logging.basicConfig to employee_test.log and several try/except blocks.
- Accept/modify/reject: Accepted. It doubles as executable documentation of the constraints.

Decisions I made and why
- Properties over ad hoc validators: one enforcement point, simpler tests.
- Read-only id: prevents accidental identity mutation during edits.
- __str__ in both classes: keeps presentation logic out of the View.

Net outcome
- I accepted most of Copilot’s output with minor tightening. The model file is I/O-free, deterministic, and exposes a clean API the rest of the app can trust.


Reflections for main.py:

Reflections — EmployeeApp.py (Controller + View + Data)

Context / prompts I used (summarized)
- I wanted a small MVC harness that keeps rules in the model, I/O in the view, and orchestration in the controller. The data layer should be “boring CSV in, CSV out,” using a role column to round-trip Manager vs Employee.

Prompt 1: View-only helpers
- What I asked: “Give me display_menu, prompts for fields, edit menu, yes/no helper, and a display_employees that just prints e.__str__() for each row.”
- Copilot’s suggestion: Small functions returning strings/ints, zero logic.
- Accepted? Yes. The View is intentionally dumb and easy to swap.

Prompt 2: Data round-trip
- What I asked: “load_employees/save_employees with DictReader/DictWriter and a role column.”
- Copilot’s suggestion: Role-based branching to build Manager or Employee; write team_size only for Manager.
- Accepted? Yes. I added a warning log for skipped malformed rows and ensured we always write a consistent header.

Prompt 3: Controller CRUD
- What I asked: “create/edit/delete/display functions; reject create on duplicate id; save after every mutation.”
- Copilot’s suggestion: Straightforward functions, letting model properties enforce rules.
- Accepted? Yes. The Controller remains small because the Model does the heavy lifting.

Prompt 4: Menu loop and logging
- What I asked: “Simple while True loop; configure logging to employee_app.log; clean exit.”
- Copilot’s suggestion: Exactly that.
- Accepted? Yes. I also echo the CSV absolute path on startup so the grader can see where the file lives.

Prompt 5: Stable CSV path and debug traces
- What I asked: “Anchor data path to the script folder so CWD doesn’t create stray CSVs; optional debug prints to show module and path.”
- Copilot’s suggestion: Use __file__ + os.path.join; os.makedirs to ensure the folder exists.
- Accepted? Yes. This eliminated the earlier issue where data was written to ./employee_data.csv at repo root.

What I learned
- When the Model owns validation and the View is I/O-only, the Controller becomes almost declarative glue. CSV round-trip with a single “role” column is enough to persist polymorphic objects. Anchoring paths to __file__ keeps dev and grading consistent across IDEs and terminals.

Net outcome
- I kept the architecture thin and obvious. The app creates/edits/deletes Employees and Managers, persists to CSV, and displays via one polymorphic path. The comments and small debug prints make it easy to trace behavior and grade.

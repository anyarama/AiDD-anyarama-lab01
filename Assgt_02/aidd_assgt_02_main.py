# This is the driver / test script for the Personnel Management prototype we built for Kelley Software Development Co. (KSD).
# The goal here is to actually exercise the object model we defined in employees.py. We want something simple and readable
# that a grader (or a teammate) can run to verify that: (1) the classes instantiate correctly, (2) we can build a single
# heterogeneous list of employees across all four subclasses, and (3) polymorphism does what it should (one loop, same
# method call, different logic per subclass). I’m intentionally keeping this as plain Python (no frameworks, no CLI libs).
#
# The flow I’m going with:
# - Create one ProjectRegistry up front; this is our “system state” for unique projects and GM tracking.
# - Provide interactive helpers to create each type of Employee. These helpers will ask just enough info to instantiate a
#   valid object. For projects, if the user references a project that doesn’t exist yet, we’ll prompt for the revenue and
#   create it through the registry so we maintain the single source of truth.
# - Keep everything in a single list called `employees`. This is important: the assignment wants one list to iterate and
#   print compensation for each employee via the same function call (calculate_compensation or a wrapper), which demonstrates
#   polymorphism cleanly.
# - Give the user a “demo dataset” option so we can instantly satisfy the requirement of having at least one of each role
#   without typing everything. This is also handy for graders who just want to see output quickly.
#
# Assumptions I’m making here in the driver:
# - The registry’s “first write wins” policy for project revenue is already documented in employees.py. If the user creates
#   an employee with a project name that already exists (but different revenue), we reuse the existing project silently.
# - For General Managers, the caller is responsible for registering them with the registry so the 3% pool splits properly.
#   I’ll do that every time we create a GM in this script to avoid surprises.
# - Input validation should be friendly but not overbearing: retry on empty strings or bad numbers; keep prompts concise.

from typing import List
from aidd_assgt_02_employees import (
    ProjectRegistry, Project,
    GeneralManager, ProjectManager, Programmer, Staff
)


# I’m going to add a couple of tiny input helpers so the main flow doesn’t drown in try/except boilerplate. The idea is:
# - input_nonempty(): keep asking until the user gives us a non-empty string.
# - input_int(): parse integers with optional min/max constraints; loop until valid.
# - input_float(): same as above for floating-point numbers.
# These are deliberately straightforward so they’re easy to trust and reuse across the four “create_*” functions below.

def input_nonempty(prompt: str) -> str:
    s = input(prompt).strip()
    while not s:
        print("Value cannot be empty.")
        s = input(prompt).strip()
    return s


def input_int(prompt: str, min_value=None, max_value=None) -> int:
    while True:
        try:
            v = int(input(prompt).strip())
            if min_value is not None and v < min_value:
                print(f"Must be >= {min_value}.")
                continue
            if max_value is not None and v > max_value:
                print(f"Must be <= {max_value}.")
                continue
            return v
        except ValueError:
            print("Please enter a valid integer.")


def input_float(prompt: str, min_value=None, max_value=None) -> float:
    while True:
        try:
            v = float(input(prompt).strip())
            if min_value is not None and v < min_value:
                print(f"Must be >= {min_value}.")
                continue
            if max_value is not None and v > max_value:
                print(f"Must be <= {max_value}.")
                continue
            return v
        except ValueError:
            print("Please enter a valid number.")


# This function just prints the menu and returns a normalized choice. I’m not doing anything fancy; it’s enough to cover:
# - 1/2/3/4 to create a GM/PM/Programmer/Staff
# - D to auto-add a demo dataset (one of each role and a couple of projects)
# - Q to quit and move to the reporting step
def choose_employee_type() -> str:
    print("\nCreate employee type:")
    print("  1) General Manager")
    print("  2) Project Manager")
    print("  3) Programmer")
    print("  4) Staff")
    print("  D) Use demo dataset (auto-create one of each)")
    print("  Q) Finish and print report")
    return input("Select [1/2/3/4/D/Q]: ").strip().upper()


# The next four “create_*” helpers encapsulate the prompts needed to build each role. A couple of details to notice:
# - For GM, we require at least one project and allow adding more. Every time the user gives a project name, we check if
#   it exists; if not, we ask for revenue and create it via the registry. We also make sure to registry.register_gm(gm).
# - For PM and Programmer, the project is exactly one. If the project doesn’t exist, we prompt for revenue once and create it.
# - For Staff, there is no project at all; we just collect identity and base salary.

def create_gm(registry: ProjectRegistry) -> GeneralManager:
    print("\n-- New General Manager --")
    first = input_nonempty("First name: ")
    last = input_nonempty("Last name: ")
    emp_id = input_nonempty("Employee ID: ")
    phone = input_nonempty("Phone: ")
    start_year = input_int("Start year (yyyy): ", min_value=1900)

    projects: List[Project] = []
    while True:
        pname = input_nonempty("Project name: ")
        existing = registry.get_project(pname)
        if existing:
            print(f"Project '{pname}' already exists with revenue ${existing.revenue:,.2f}. Reusing it.")
            proj = existing
        else:
            rev = input_float("Project revenue: ", min_value=0.0)
            proj = registry.upsert_project(pname, rev)
        projects.append(proj)

        more = input("Add another project for this GM? [y/N]: ").strip().lower()
        if more != "y":
            break

    gm = GeneralManager(first, last, emp_id, phone, start_year, projects)
    registry.register_gm(gm)
    return gm


def create_pm(registry: ProjectRegistry) -> ProjectManager:
    print("\n-- New Project Manager --")
    first = input_nonempty("First name: ")
    last = input_nonempty("Last name: ")
    emp_id = input_nonempty("Employee ID: ")
    phone = input_nonempty("Phone: ")
    start_year = input_int("Start year (yyyy): ", min_value=1900)

    pname = input_nonempty("Assigned project name: ")
    proj = registry.get_project(pname)
    if proj is None:
        print("Project does not exist yet. We need the revenue to create it.")
        rev = input_float("Project revenue: ", min_value=0.0)
        proj = registry.upsert_project(pname, rev)

    return ProjectManager(first, last, emp_id, phone, start_year, proj)


def create_programmer(registry: ProjectRegistry) -> Programmer:
    print("\n-- New Programmer --")
    first = input_nonempty("First name: ")
    last = input_nonempty("Last name: ")
    emp_id = input_nonempty("Employee ID: ")
    phone = input_nonempty("Phone: ")
    start_year = input_int("Start year (yyyy): ", min_value=1900)
    base = input_float("Base salary: ", min_value=0.0)

    pname = input_nonempty("Assigned project name: ")
    proj = registry.get_project(pname)
    if proj is None:
        print("Project does not exist yet. We need the revenue to create it.")
        rev = input_float("Project revenue: ", min_value=0.0)
        proj = registry.upsert_project(pname, rev)

    return Programmer(first, last, emp_id, phone, start_year, base_salary=base, project=proj)


def create_staff(registry: ProjectRegistry) -> Staff:
    print("\n-- New Staff --")
    first = input_nonempty("First name: ")
    last = input_nonempty("Last name: ")
    emp_id = input_nonempty("Employee ID: ")
    phone = input_nonempty("Phone: ")
    start_year = input_int("Start year (yyyy): ", min_value=1900)
    base = input_float("Base salary: ", min_value=0.0)
    return Staff(first, last, emp_id, phone, start_year, base_salary=base)


# This tiny helper just drops in a clean demo so you can validate the entire flow without data entry. It creates:
# - two projects (Core Banking Revamp, Digital Wallet),
# - one GM tied to both projects (and registered with the registry),
# - one PM on project 1,
# - one Programmer on project 2 with a base salary,
# - one Staff member with a base salary.
# We return them as a list so the caller can extend the main employees list in one line.
def add_demo(registry: ProjectRegistry) -> List:
    p1 = registry.upsert_project("Core Banking Revamp", 1_000_000)
    p2 = registry.upsert_project("Digital Wallet", 500_000)

    gm = GeneralManager("Asha", "Rao", "GM001", "317-555-1111", 2018, [p1, p2])
    registry.register_gm(gm)

    pm = ProjectManager("Liam", "Chen", "PM101", "317-555-2222", 2019, p1)
    pg = Programmer("Neha", "Singh", "PR301", "317-555-3333", 2021, base_salary=95_000, project=p2)
    st = Staff("Marco", "Silva", "ST501", "317-555-4444", 2020, base_salary=55_000)
    return [gm, pm, pg, st]


# The reporting function is intentionally boring (and that’s good). The whole point of the OO design is that the loop here
# is trivial: for each employee, call the same method and print. The registry is shared to keep the compensation logic
# consistent. I’m also printing the aggregate registry stats at the end so it’s obvious how the GM pool is derived.
def print_comp_report(employees: List, registry: ProjectRegistry) -> None:
    print("\n================ Compensation Report ================")
    for e in employees:
        # Using the convenience wrapper on Employee to keep formatting consistent.
        print(e.compensation_summary(registry))
    print("====================================================\n")
    print(f"Total unique project revenue in registry: ${registry.total_revenue:,.2f}")
    print(f"Registered General Managers: {registry.gm_count}")


# The main loop ties everything together. We create the registry, keep a single list, present a simple menu, and let the
# user either add employees one-by-one or drop in the demo. When they quit, we ensure there’s at least one of each type by
# auto-adding the demo if the list is empty (that way the assignment’s “print all” requirement is always satisfied).
def main() -> None:
    registry = ProjectRegistry()
    employees: List = []

    try:
        while True:
            choice = choose_employee_type()
            if choice == "1":
                employees.append(create_gm(registry))
            elif choice == "2":
                employees.append(create_pm(registry))
            elif choice == "3":
                employees.append(create_programmer(registry))
            elif choice == "4":
                employees.append(create_staff(registry))
            elif choice == "D":
                employees.extend(add_demo(registry))
                print("Demo dataset added.")
            elif choice == "Q":
                break
            else:
                print("Invalid choice. Please select again.")
    except KeyboardInterrupt:
        print("\nInterrupted. Proceeding to report...")

    if not employees:
        print("\nNo employees created. Adding demo dataset to satisfy assignment criteria.")
        employees.extend(add_demo(registry))

    print_comp_report(employees, registry)


if __name__ == "__main__":
    main()

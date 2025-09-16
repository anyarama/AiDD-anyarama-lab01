############################################  Prompt for employees.py ############################################ 

 We have to develop a code for Kelley Software Development Co.(KSD) to create a simple prototype that demonstrates the basic
functionality of a personnel Management system. The program should have a Employee parent class with four subclasses
 - 1. GeneralManager()
 - 2. ProjectManager()
 - 3. Programmer()
 - 4. Staff()
We should start with an Employee() superclass and four subclasses GeneralManager(), ProjectManager(), Programmer(), Staff()
The system required different information for different kinds of employees, so we need to design the classes accordingly.
GeneralManager: first_name, last_name, emp_id, phone, start_year, projects (≥1); each unique project has revenue.
ProjectManager (exactly one project): project (1), revenue, first_name, last_name, emp_id, phone, start_year.
Programmer: project (1), project revenue, first_name, last_name, emp_id, phone, base_salary, start_year.
Staff: first_name, last_name, emp_id, phone, base_salary, start_year.
We have to put only the truly universal attributes + logic in the superclass, and push everything else down.
Since first_name, last_name, emp_id, phone, start_year are common to all employees, they will be in the Employee superclass.
ASSUMPTIONS:
 - All General Managers share 3% of total revenue across ALL unique projects; the pool is split equally among all GMs.
 - Projects are uniquely identified by normalized project name (lowercased, stripped). "First write wins" for revenue.
 - No mutable module-level globals: ProjectRegistry is the system’s single source of truth for projects + GM count.
 - Printing of total compensation is supported via Employee.compensation_summary(), but each subclass owns its calc logic.

prompts I used:

 ===========================================================================================
 Prompt to Copilot: Create a lightweight Project value-object with validation
 Goals:
   - Define a frozen dataclass Project(name: str, revenue: float)
   - Validate that name is non-empty and revenue is non-negative in __post_init__
   - Implement __str__ to show a friendly representation "Project(name=..., revenue=...)".
 Constraints:
   - Use @dataclass(frozen=True) so instances are immutable
   - Keep logic minimal; heavy aggregates belong to ProjectRegistry
 ===========================================================================================

 ===========================================================================================
 Prompt to Copilot: Build ProjectRegistry to deduplicate projects and track GMs
 Goals:
   - Maintain a dict of unique Project objects keyed by normalized name
   - Expose upsert_project(name, revenue) with first-write-wins policy
   - Provide get_project(name), total_revenue (sum of all unique), gm_count
   - Track registered General Managers via register_gm(gm)
 Constraints:
   - Normalize names via helper _key(name) -> lower/strip
   - No global mutable state; this object is the single source of truth
 ===========================================================================================

 ===========================================================================================
 Prompt to Copilot: Create the Parent Employee Class
 Based on the comments I provided, create the Employee parent class. It should:
   - Import the datetime module at the top of the file (already done) and define CURRENT_YEAR.
   - The __init__ method should accept first_name, last_name, emp_id, phone, and start_year.
   - Normalize phone to digits only; validate names/ID are non-empty and start_year <= CURRENT_YEAR.
   - Include a placeholder/abstract method calculate_compensation(registry) that child classes must implement.
   - Include a placeholder/abstract __str__() method.
   - Provide a years_of_service property and a helper compensation_summary(registry) that formats output.
 Constraints:
   - Use ABC and @abstractmethod to enforce subclass overrides.
 ===========================================================================================

 ===========================================================================================
 Prompt to Copilot: Implement GeneralManager subclass
 Goals:
   - Constructor must accept (first_name, last_name, emp_id, phone, start_year, projects: List[Project])
   - Validate that projects list is non-empty
   - calculate_compensation(registry): return equal share of 3% of registry.total_revenue across all GMs
   - __str__() should include role tag, name/ID, and project names joined by comma
 Constraints:
   - Use registry.gm_count defensively (treat 0 as 1 to avoid ZeroDivisionError)
 ===========================================================================================


 ===========================================================================================
 Prompt to Copilot: Implement ProjectManager subclass
 Goals:
   - Constructor must accept (first_name, last_name, emp_id, phone, start_year, project: Project)
   - calculate_compensation(registry): return 5% of that single project's revenue
   - __str__() should include role tag, name/ID, and the project name
 Constraints:
   - Exactly one project per PM
 ===========================================================================================

 ===========================================================================================
 Prompt to Copilot: Implement Programmer subclass
 Goals:
   - Constructor must accept (first_name, last_name, emp_id, phone, start_year, base_salary: float, project: Project)
   - Validate base_salary >= 0 using a property setter
   - calculate_compensation(registry): base_salary + 1% of that project's revenue
   - __str__() shows role tag, name/ID, base salary, and project name
 Constraints:
   - Exactly one project per Programmer
 ===========================================================================================

 ===========================================================================================
 Prompt to Copilot: Implement Staff subclass
 Goals:
   - Constructor must accept (first_name, last_name, emp_id, phone, start_year, base_salary: float)
   - Validate base_salary >= 0 using a property setter
   - calculate_compensation(registry): base_salary + (100 * years_of_service)
   - __str__() shows role tag, name/ID, and base salary
 Constraints:
   - No project association for Staff
 ===========================================================================================
 ############################################  Prompt for main.py ############################################ 

 
This is the driver / test script for the Personnel Management prototype we built for Kelley Software Development Co. (KSD).
 The goal here is to actually exercise the object model we defined in employees.py. We want something simple and readable
 that a grader (or a teammate) can run to verify that: (1) the classes instantiate correctly, (2) we can build a single
 heterogeneous list of employees across all four subclasses, and (3) polymorphism does what it should (one loop, same
 method call, different logic per subclass). I’m intentionally keeping this as plain Python (no frameworks, no CLI libs).

 The flow I’m going with:
 - Create one ProjectRegistry up front; this is our “system state” for unique projects and GM tracking.
 - Provide interactive helpers to create each type of Employee. These helpers will ask just enough info to instantiate a
   valid object. For projects, if the user references a project that doesn’t exist yet, we’ll prompt for the revenue and
   create it through the registry so we maintain the single source of truth.
 - Keep everything in a single list called `employees`. This is important: the assignment wants one list to iterate and
   print compensation for each employee via the same function call (calculate_compensation or a wrapper), which demonstrates
   polymorphism cleanly.
 - Give the user a “demo dataset” option so we can instantly satisfy the requirement of having at least one of each role
   without typing everything. This is also handy for graders who just want to see output quickly.

 Assumptions I’m making here in the driver:
 - The registry’s “first write wins” policy for project revenue is already documented in employees.py. If the user creates
   an employee with a project name that already exists (but different revenue), we reuse the existing project silently.
 - For General Managers, the caller is responsible for registering them with the registry so the 3% pool splits properly.
   I’ll do that every time we create a GM in this script to avoid surprises.
 - Input validation should be friendly but not overbearing: retry on empty strings or bad numbers; keep prompts concise.

Prompt 1:
# I’m going to add a couple of tiny input helpers so the main flow doesn’t drown in try/except boilerplate. The idea is:
# - input_nonempty(): keep asking until the user gives us a non-empty string.
# - input_int(): parse integers with optional min/max constraints; loop until valid.
# - input_float(): same as above for floating-point numbers.
# These are deliberately straightforward so they’re easy to trust and reuse across the four “create_*” functions below.

Prompt 2:
# This function just prints the menu and returns a normalized choice. I’m not doing anything fancy; it’s enough to cover:
# - 1/2/3/4 to create a GM/PM/Programmer/Staff
# - D to auto-add a demo dataset (one of each role and a couple of projects)
# - Q to quit and move to the reporting step

Prompt 3:

# The next four “create_*” helpers encapsulate the prompts needed to build each role. A couple of details to notice:
# - For GM, we require at least one project and allow adding more. Every time the user gives a project name, we check if
#   it exists; if not, we ask for revenue and create it via the registry. We also make sure to registry.register_gm(gm).
# - For PM and Programmer, the project is exactly one. If the project doesn’t exist, we prompt for revenue once and create it.
# - For Staff, there is no project at all; we just collect identity and base salary.

Prompt 4:

# This tiny helper just drops in a clean demo so you can validate the entire flow without data entry. It creates:
# - two projects (Core Banking Revamp, Digital Wallet),
# - one GM tied to both projects (and registered with the registry),
# - one PM on project 1,
# - one Programmer on project 2 with a base salary,
# - one Staff member with a base salary.
# We return them as a list so the caller can extend the main employees list in one line.

Prompt 5:

# The reporting function is intentionally boring (and that’s good). The whole point of the OO design is that the loop here
# is trivial: for each employee, call the same method and print. The registry is shared to keep the compensation logic
# consistent. I’m also printing the aggregate registry stats at the end so it’s obvious how the GM pool is derived.

Prompt 6:

# The main loop ties everything together. We create the registry, keep a single list, present a simple menu, and let the
# user either add employees one-by-one or drop in the demo. When they quit, we ensure there’s at least one of each type by
# auto-adding the demo if the list is empty (that way the assignment’s “print all” requirement is always satisfied).

Reflections for employees.py:

Reflections — AiDD_Assgt-02_employees.py

Context / prompts I used (summarized in my own words)
- I asked Copilot to help me implement a small personnel management model for KSD using an Employee superclass and four subclasses (GeneralManager, ProjectManager, Programmer, Staff). I specified the attributes and compensation rules for each role. I also asked for a lightweight, immutable Project value object and a ProjectRegistry that deduplicates projects and tracks GMs. I was explicit that only truly universal fields live in Employee (first_name, last_name, emp_id, phone, start_year) and that all compensation logic must be implemented in the subclasses. I added assumptions: 3% GM pool split equally, first-write-wins revenue in the registry, and no mutable globals. I wanted helpful __str__ methods and a small helper for printing compensation.

What I asked Copilot for component by component, what it suggested, and what I did with the suggestions

1) Project value object
- Prompt I gave: “Create a frozen dataclass Project(name: str, revenue: float) with simple validation in __post_init__ (name non-empty, revenue non-negative) and a friendly __str__.”
- Copilot’s suggestion: A @dataclass(frozen=True) with __post_init__ checks and a straightforward __str__.
- Accept/modify/reject: Accepted almost verbatim. I kept __str__ with formatted revenue (commas) for nicer output.
- What I learned: Keeping Project immutable avoids accidental revenue drift and makes the registry logic safer.

2) ProjectRegistry (dedupe + GM tracking)
- Prompt I gave: “Build a registry that stores unique projects keyed by normalized name (lower/strip). Provide upsert_project(name, revenue) with first-write-wins, get_project(name), total_revenue, and a way to register GMs and count them.”
- Copilot’s suggestion: A dict-backed registry, _key() normalizer, upsert/get, properties for totals and gm_count, plus a register_gm method.
- Accept/modify/reject: Accepted. I reiterated the “first write wins” policy in comments so behavior is predictable. No globals—everything hangs off the registry instance.
- What I learned: Centralizing cross-cutting state (projects, GM count) in one place simplifies compensation math and testability.

3) Employee superclass (universal identity + contract)
- Prompt I gave: “Create an abstract Employee with __init__(first, last, emp_id, phone, start_year), digits-only phone normalization, validation for empties/future years, a years_of_service property, abstract calculate_compensation(registry), abstract __str__(), and a small convenience method compensation_summary(registry).”
- Copilot’s suggestion: An ABC with the exact interface, phone normalization helper, and the properties I asked for.
- Accept/modify/reject: Accepted. I kept the method names in snake_case to follow PEP 8. I also enforced start_year <= CURRENT_YEAR and digit-only phone storage.
- What I learned: Pushing only universal logic into the base class keeps subclasses lean and prevents LSP violations (e.g., not forcing salary/project onto roles that don’t have them).

4) GeneralManager subclass (3% pool, equal split)
- Prompt I gave: “GM requires >= 1 project and gets an equal share of a 3% pool across all unique projects. Use registry.total_revenue and registry.gm_count; defend against 0 by treating it as 1.”
- Copilot’s suggestion: Constructor validating projects list, calculate_compensation using (0.03 * total) / max(1, gm_count), and a __str__ showing project names.
- Accept/modify/reject: Accepted. The defensive max(1, gm_count) is there to prevent a ZeroDivisionError if a caller forgets to register GMs, but I still plan to register every GM in the driver.
- What I learned: Pool math belongs here, not in the driver. Encapsulation keeps business rules close to the data.

5) ProjectManager subclass (5% of single project)
- Prompt I gave: “Exactly one project; compensation is 5% of that project’s revenue.”
- Copilot’s suggestion: Minimal constructor with a single Project, simple percentage calc, and a readable __str__.
- Accept/modify/reject: Accepted as is.
- What I learned: The consistent method signature (calculate_compensation(registry)) across roles keeps the polymorphic loop trivial even when a role doesn’t need the registry.

6) Programmer subclass (base + 1% of project)
- Prompt I gave: “Programmer has base_salary >= 0 (use property for validation) and exactly one project; total is base + 1% project revenue.”
- Copilot’s suggestion: Property with guard for non-negative base salary, calculation method, and a __str__ including base and project.
- Accept/modify/reject: Accepted. I ensured floats are cast in the setter to avoid type surprises.
- What I learned: Properties are a clean way to keep invariants without changing how callers assign attributes.

7) Staff subclass (base + $100 × years_of_service)
- Prompt I gave: “No project; base_salary >= 0; years_of_service drawn from Employee; compute base + 100 * years.”
- Copilot’s suggestion: Straightforward field + property validation and the compensation formula.
- Accept/modify/reject: Accepted. Kept the __str__ consistent with other roles.
- What I learned: Reusing the base class’ years_of_service keeps the rule single-sourced.

Decisions I made and why
- “First write wins” for project revenue: I chose predictability over magical updates. If I need “latest wins,” that’s an explicit change rather than an accidental side effect of calling upsert.
- No module-level mutable globals: The registry is the boundary for shared state. This keeps tests simpler and avoids hidden couplings.
- One polymorphic API: calculate_compensation(registry) + __str__() across all roles makes downstream code extremely simple.

Net outcome
- I accepted the majority of Copilot’s suggestions with small tweaks to naming, formatting, and comments. The final code matches the assignment rules, is easy to test, and reads clearly. Most importantly, the compensation logic for each role lives in that role, and the base class stays clean.


Reflections for main.py:


Reflections — main.py (driver)

Context / prompts I used (summarized)
- I wanted a small, no-framework driver that proves the OO design: create a single ProjectRegistry, interactively add employees across all four roles, push them into one list, and then print a compensation report by iterating that list (polymorphism). I also wanted a demo dataset option so graders can see output fast without typing.

Prompt 1: tiny input helpers
- What I asked: “Give me input_nonempty, input_int(min/max), input_float(min/max) so I don’t litter the code with try/except.”
- Copilot’s suggestion: Simple loops that re-prompt on invalid input, with optional bounds for numeric functions.
- Accepted? Yes. These helpers keep the ‘create_*’ functions readable.

Prompt 2: the menu function
- What I asked: “A minimal menu that returns 1/2/3/4/D/Q for the four roles, demo, and quit.”
- Copilot’s suggestion: A print block with a normalized upper-cased return value.
- Accepted? Yes. Kept it simple and obvious.

Prompt 3: the four create_* functions
- What I asked: “Encapsulate prompts and object creation for GM/PM/Programmer/Staff. For GM: support multiple projects and register the GM. For PM/Programmer: exactly one project; if it doesn’t exist, prompt for revenue and create it. For Staff: no project; just base salary.”
- Copilot’s suggestion: Four small functions. Each one uses the registry to dedupe projects and to register GMs.
- Accepted? Yes, with small wording tweaks in prompts and messages. This pattern keeps business rules out of the driver and leverages the registry correctly.

Prompt 4: add_demo
- What I asked: “Create two projects and one of each role wired to those projects to showcase all compensation rules.”
- Copilot’s suggestion: A neat demo that mirrors the example I described (Core Banking Revamp, Digital Wallet, GM on both).
- Accepted? Yes. This ensures the assignment is runnable even if no interactive input is provided.

Prompt 5: print_comp_report
- What I asked: “A boring, reliable loop that prints a line per employee and then two registry stats (total revenue and GM count).”
- Copilot’s suggestion: Iterate the employees list and call e.compensation_summary(registry).
- Accepted? Yes. I intentionally leaned into “boring” because that’s a sign the design is clean.

Prompt 6: main loop
- What I asked: “Stitch it all together: build the registry, keep one list, loop on the menu, support Ctrl+C without losing work, and auto-add the demo if the user quits without creating anything.”
- Copilot’s suggestion: A straightforward while loop with a KeyboardInterrupt guard and the demo fallback.
- Accepted? Yes. This keeps the user experience smooth and the assignment’s ‘one list + print’ requirement always satisfied.

Extra: dynamic import for a hyphenated module name
- What I asked: “The employees file is named ‘AiDD_Assgt-02_employees.py’. Normal Python imports don’t like hyphens. Load it dynamically with importlib and bind the classes to local names so the rest of the file doesn’t change.”
- Copilot’s suggestion: Use importlib.util.spec_from_file_location, module_from_spec, and exec_module, then expose ProjectRegistry/Project/etc.
- Accepted? Yes. Works well. If I ever rename the file to underscores, I can delete the dynamic import block and use a normal ‘from … import …’.

What I learned
- Keeping the driver dumb and the classes smart is the right trade-off. The registry makes all the compensation math deterministic and prevents revenue double counting. The single polymorphic API means the final report function is basically just a for-loop. Also, handling the hyphenated filename with a dynamic import is a pragmatic workaround when you can’t rename files to be Python-friendly.

Net outcome
- I accepted most of Copilot’s output with minor edits for clarity and consistency. The driver now demonstrates object creation, deduped projects, GM registration, and polymorphic compensation reporting. It’s easy to grade and easy to extend.

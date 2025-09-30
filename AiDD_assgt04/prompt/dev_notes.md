# Developer Notes — EmployeeApp.py (Controller)

**Scope:** Quick-reference notes for maintainers. This clarifies how the Controller coordinates MVC flows for Assignment 4 (SQLite).

---

## 1) Role in MVC
- **Controller (EmployeeApp.py)**: Orchestrates flows; defers persistence to DAL and I/O to View.
- **Model (`employee.py`)**: Validation, immutability, polymorphism.
- **Data (`EmployeeData_sqlite.py`)**: SQLite persistence and object mapping.
- **View (`EmployeeView.py`)**: Console prompts and display.

> Design rule: business rules live here; SQL never does.

---

## 2) Startup Sequence
1. `data.init_db()` ensures `employees.sqlite` + schema exist.
2. (Optional) Print active DB path via `data.get_db_path()` to avoid path confusion.
3. Enter menu loop and dispatch commands.

---

## 3) Controller Handlers
### create_or_edit()
- Collects fields via View, constructs `Employee` or `Manager`.
- Persists through `data.upsert_employee()`.
- Catches `ValidationError` and echoes readable messages.

### edit_existing()
- Loads record by ID, shows current state, updates all but **ID** (immutable).
- Supports changing role to/from Manager; prompts for `team_size` when needed.
- Reconstructs and upserts the object.

### delete_existing()
- Idempotent delete by ID via DAL.

### display_all()
- Lists all via DAL; View prints polymorphic `__str__` outputs.

---

## 4) Validation & Errors
- Validation belongs to Model (`employee.py`).
- Typical failures: department not `[A-Z]{3}`; phone not 10 digits after sanitize; `team_size` not int.
- Controller surfaces errors; do not swallow them.

---

## 5) DAL Contract
- Absolute DB path pinned inside DAL; Controller never imports `sqlite3`.
- Available calls: `init_db`, `get_db_path`, `list_employees`, `get_employee`, `upsert_employee`, `delete_employee`.

---

## 6) Common Pitfalls
- Wrong DB file: check the printed path.
- “no such table: employees”: forgot `init_db()` or wrong working directory.
- Validation loops: fix input; do not bypass Model rules.

---

## 7) Smoke Test
```bash
python3 EmployeeApp.py
# 1) Add E1 (ENG, 1234567890); 1) Add M1 (team_size=3)
# 4) Display; 2) Edit M1 team_size -> 6; 3) Delete E1
sqlite3 "$(python3 - <<'PY'
import EmployeeData_sqlite as d;print(d.get_db_path())
PY)" "SELECT COUNT(*) FROM employees;"
```

---

## 8) Extensibility Ideas
- Search endpoints; bulk import/export; structured logging; pytest with in-memory DB.
- CLI flags or env var to switch persistence (e.g., CSV vs SQLite) if needed later.

---

## 9) Submission Checklist (A4)
- Part 1: `Day08_SQLite_Exercise.sql` (+ optional `Day08_verification.txt`).
- Part 2: `employee.py`, `EmployeeView.py`, `EmployeeApp.py`, `EmployeeData_sqlite.py`, `README_AiDD_Assgt4.md`.

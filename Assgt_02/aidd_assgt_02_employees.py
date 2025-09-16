# We have to develop a code for Kelley Software Development Co.(KSD) to create a simple prototype that demonstrates the basic
# functionality of a personnel Management system. The program should have a Employee parent class with four subclasses
# 1. GeneralManager()
# 2. ProjectManager()
# 3. Programmer()
# 4. Staff()
# We should start with an Employee() superclass and four subclasses GeneralManager(), ProjectManager(), Programmer(), Staff()
# The system required different information for different kinds of employees, so we need to design the classes accordingly.
# GeneralManager: first_name, last_name, emp_id, phone, start_year, projects (≥1); each unique project has revenue.
# ProjectManager (exactly one project): project (1), revenue, first_name, last_name, emp_id, phone, start_year.
# Programmer: project (1), project revenue, first_name, last_name, emp_id, phone, base_salary, start_year.
# Staff: first_name, last_name, emp_id, phone, base_salary, start_year.
# We have to put only the truly universal attributes + logic in the superclass, and push everything else down.
# Since first_name, last_name, emp_id, phone, start_year are common to all employees, they will be in the Employee superclass.
# Assumptions I am making to keep this prototype consistent with the assignment: projects are unique by name after lowercasing
# and trimming; the first time we see a project name, the revenue we set for it becomes the single source of truth; any later
# attempt to “recreate” the same project just reuses the existing one. Also, General Managers share 3% of the total revenue
# across all unique projects and that pool is split equally across all GMs that have been registered with the registry. No
# module-level global mutable state; everything that needs to be shared system-wide (projects, GM count) sits inside a
# ProjectRegistry instance so that tests and demos are deterministic.

from __future__ import annotations
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

CURRENT_YEAR = date.today().year


# This class is the tiny “value object” for a project. It’s intentionally small and immutable so we don’t end up with
# drifting state. The only two things we care about at this level are the project’s human-readable name and its revenue.
# Validation is straightforward: the name must exist (not blank/whitespace) and revenue cannot be negative. We keep __str__
# friendly because we’ll probably log or print these in the test driver. Any bigger aggregates (like total revenue) are not
# this class’s job; those live in the registry below.
@dataclass(frozen=True)
class Project:
    name: str
    revenue: float

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Project name cannot be empty.")
        if self.revenue < 0:
            raise ValueError("Project revenue cannot be negative.")

    def __str__(self) -> str:
        return f"Project(name={self.name}, revenue={self.revenue:,.2f})"


# This registry exists so we have one canonical place that knows “what projects exist” and “who the general managers are”.
# The assignment’s compensation rules depend on the sum of revenue across ALL UNIQUE projects, so we must deduplicate by a
# normalized key. I’m normalizing by lowercasing and stripping the project name. I’m also capturing every GM that gets
# created so we can split the 3% pool equally. The policy I’m going with is “first write wins” for project revenue: the
# first time a project is upserted, that revenue sticks; subsequent upserts with the same normalized name will return the
# already-existing Project object and ignore the new revenue (if you want “latest write wins” it’s a one-line change, but
# I’m documenting the current choice so the behavior is predictable).
class ProjectRegistry:
    def __init__(self) -> None:
        self._projects: Dict[str, Project] = {}
        self._general_managers: List["GeneralManager"] = []

    @staticmethod
    def _key(name: str) -> str:
        return name.strip().lower()

    def upsert_project(self, name: str, revenue: float) -> Project:
        # Insert-or-return behavior. If we’ve already seen this normalized name, we just return the existing Project so we
        # don’t accidentally double-count revenue. Otherwise, we create a new immutable Project and store it.
        k = self._key(name)
        if k in self._projects:
            return self._projects[k]
        proj = Project(name=name.strip(), revenue=float(revenue))
        self._projects[k] = proj
        return proj

    def get_project(self, name: str) -> Optional[Project]:
        # Convenience for drivers: fetch by name without worrying about case or leading/trailing spaces.
        return self._projects.get(self._key(name))

    def register_gm(self, gm: "GeneralManager") -> None:
        # The GM list is purely for counting (so we can split the 3% pool fairly). We also defend against duplicates.
        if gm not in self._general_managers:
            self._general_managers.append(gm)

    @property
    def total_revenue(self) -> float:
        # Sum across the unique projects in the catalog. Because Project is frozen, this is stable during a run.
        return sum(p.revenue for p in self._projects.values())

    @property
    def gm_count(self) -> int:
        # Simple count for splitting the pool. If nobody registered, the GM code will defensively treat it as 1.
        return len(self._general_managers)


# The Employee superclass carries only the fields and behaviors that truly every employee shares: first name, last name,
# employee id, phone (stored in digits-only form to avoid formatting problems), and start year. It also owns simple shared
# utilities: normalizing phone numbers and computing years of service relative to CURRENT_YEAR. We do not put base salary or
# project references here because not all employees have those. This class is abstract because each subtype is required to
# implement its own compensation logic and its own string representation. Keeping the API uniform lets us throw instances
# of any subclass into a single list and still iterate and call the same methods (polymorphism). The little helper
# compensation_summary is there simply so you can print a consistent report line without repeating formatting everywhere.
class Employee(ABC):
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int) -> None:
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.emp_id = emp_id.strip()
        self._phone = self._normalize_phone(phone)
        if start_year > CURRENT_YEAR:
            raise ValueError("start_year cannot be in the future.")
        self.start_year = int(start_year)

        if not self.first_name:
            raise ValueError("first_name cannot be empty.")
        if not self.last_name:
            raise ValueError("last_name cannot be empty.")
        if not self.emp_id:
            raise ValueError("emp_id cannot be empty.")

    @property
    def phone(self) -> str:
        # We store phones as digits only. If you need (xxx) formatting, do it at the output boundary.
        return self._phone

    @phone.setter
    def phone(self, v: str) -> None:
        self._phone = self._normalize_phone(v)

    @staticmethod
    def _normalize_phone(v: str) -> str:
        # Strip everything except digits. Keeps the data layer clean and comparable.
        return "".join(ch for ch in str(v) if ch.isdigit())

    @property
    def years_of_service(self) -> int:
        # Used by the Staff compensation rule and handy for reporting anywhere else.
        return max(0, CURRENT_YEAR - self.start_year)

    @abstractmethod
    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        # Every subclass has a different rule, so the base class just defines the contract.
        # The registry gives access to the “system” state (unique projects, total revenue, GM count).
        ...

    @abstractmethod
    def __str__(self) -> str:
        # Give each subclass control of how it should appear in a report or log line.
        ...

    def compensation_summary(self, registry: ProjectRegistry) -> str:
        # A friendly, uniform one-liner for reports that depends on the subclass calculation.
        total = self.calculate_compensation(registry)
        return f"{self} | Total Compensation: ${total:,.2f}"


# A General Manager is associated with one or more projects (list). Per the assignment, their pay is not tied to any single
# project but to the entire portfolio: all General Managers share a pool equal to 3% of the total revenue across all unique
# projects in the system. That pool is split equally among GMs. We rely on the ProjectRegistry to provide both the total
# revenue and the count of registered GMs. If a driver forgets to register a GM, we still guard against division by zero
# (treat it as one) so the demo code won’t blow up; that said, registering GMs is expected usage.
class GeneralManager(Employee):
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 projects: List[Project]) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        if not projects:
            raise ValueError("GeneralManager must be associated with at least one project.")
        self._projects = list(projects)

    @property
    def projects(self) -> List[Project]:
        # Defensive copy because callers shouldn’t be able to mutate our internal list.
        return list(self._projects)

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        pool = 0.03 * registry.total_revenue
        n = max(1, registry.gm_count)
        return pool / n

    def __str__(self) -> str:
        pnames = ", ".join(p.name for p in self._projects)
        return f"[GM] {self.first_name} {self.last_name} (ID {self.emp_id}) | Projects: {pnames}"


# A Project Manager is tied to exactly one project. Their compensation is 5% of that project’s revenue. The registry is not
# strictly necessary for this math since we read from the one project object we already hold, but we keep the same signature
# to maintain a consistent API across all subclasses. The driver code becomes trivial when every employee exposes the same
# method and return type.
class ProjectManager(Employee):
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 project: Project) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        self._project = project

    @property
    def project(self) -> Project:
        return self._project

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        return 0.05 * self._project.revenue

    def __str__(self) -> str:
        return f"[PM] {self.first_name} {self.last_name} (ID {self.emp_id}) | Project: {self._project.name}"


# A Programmer is also tied to exactly one project, but unlike the PM, there is a base salary involved. The rule is:
# base_salary + 1% of that project’s revenue. Base salary is guarded through a property so we can enforce non-negative
# values at the boundary. Again, we keep the same method signature for polymorphism even though the registry is not needed
# for the math here.
class Programmer(Employee):
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 base_salary: float, project: Project) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        self.base_salary = float(base_salary)  # route through property for validation
        self._project = project

    @property
    def base_salary(self) -> float:
        return self._base_salary

    @base_salary.setter
    def base_salary(self, v: float) -> None:
        v = float(v)
        if v < 0:
            raise ValueError("Base salary cannot be negative.")
        self._base_salary = v

    @property
    def project(self) -> Project:
        return self._project

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        return self._base_salary + 0.01 * self._project.revenue

    def __str__(self) -> str:
        return (f"[Programmer] {self.first_name} {self.last_name} (ID {self.emp_id}) | "
                f"Base ${self._base_salary:,.2f} | Project: {self._project.name}")


# Staff are the simplest case: there is no project association at all. Their compensation is their base salary plus a small
# tenure kicker: $100 for every year of service (computed from CURRENT_YEAR − start_year, never negative). We validate base
# salary the same way we did for Programmer so bad inputs get caught early.
class Staff(Employee):
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 base_salary: float) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        self.base_salary = float(base_salary)

    @property
    def base_salary(self) -> float:
        return self._base_salary

    @base_salary.setter
    def base_salary(self, v: float) -> None:
        v = float(v)
        if v < 0:
            raise ValueError("Base salary cannot be negative.")
        self._base_salary = v

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        return self._base_salary + (100.0 * self.years_of_service)

    def __str__(self) -> str:
        return f"[Staff] {self.first_name} {self.last_name} (ID {self.emp_id}) | Base ${self._base_salary:,.2f}"

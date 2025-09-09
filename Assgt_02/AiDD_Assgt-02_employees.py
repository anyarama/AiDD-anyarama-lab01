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
# ASSUMPTIONS:
# - All General Managers share 3% of total revenue across ALL unique projects; the pool is split equally among all GMs.
# - Projects are uniquely identified by normalized project name (lowercased, stripped). "First write wins" for revenue.
# - No mutable module-level globals: ProjectRegistry is the system’s single source of truth for projects + GM count.
# - Printing of total compensation is supported via Employee.compensation_summary(), but each subclass owns its calc logic.

from __future__ import annotations
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

CURRENT_YEAR = date.today().year


# Project represents a unique project with a single source of truth for revenue.
# Each unique project has exactly one revenue value in the system.
@dataclass(frozen=True)
class Project:
    # Project name (unique key, normalized by registry) and revenue (non-negative)
    name: str
    revenue: float

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Project name cannot be empty.")
        if self.revenue < 0:
            raise ValueError("Project revenue cannot be negative.")

    def __str__(self) -> str:
        return f"Project(name={self.name}, revenue={self.revenue:,.2f})"


class ProjectRegistry:
    # ProjectRegistry maintains a de-duplicated catalog of projects and tracks GM registrations.
    # Why: We must sum revenue across ALL UNIQUE projects (avoid double counting), and we need the GM count
    # to split the 3% pool fairly across all General Managers.
    def __init__(self) -> None:
        self._projects: Dict[str, Project] = {}
        self._general_managers: List["GeneralManager"] = []

    @staticmethod
    def _key(name: str) -> str:
        # Normalize project name to ensure uniqueness
        return name.strip().lower()

    def upsert_project(self, name: str, revenue: float) -> Project:
        # First-write-wins: if a project name already exists, return the existing project (ignore new revenue).
        k = self._key(name)
        if k in self._projects:
            return self._projects[k]
        proj = Project(name=name.strip(), revenue=float(revenue))
        self._projects[k] = proj
        return proj

    def get_project(self, name: str) -> Optional[Project]:
        # Fetch by name (case-insensitive). Returns None if not found.
        return self._projects.get(self._key(name))

    def register_gm(self, gm: "GeneralManager") -> None:
        # Track General Managers so the 3% pool can be divided equally among all GMs.
        if gm not in self._general_managers:
            self._general_managers.append(gm)

    @property
    def total_revenue(self) -> float:
        # Sum of revenue across all UNIQUE projects
        return sum(p.revenue for p in self._projects.values())

    @property
    def gm_count(self) -> int:
        # Number of registered GMs; defensive code will treat 0 as 1 when splitting the pool.
        return len(self._general_managers)


class Employee(ABC):
    # Employee is the superclass (parent) that centralizes universal identity + tenure logic.
    # UNIVERSAL FIELDS: first_name, last_name, emp_id, phone, start_year
    # SHARED UTILITIES: phone normalization, years_of_service computation
    # CONTRACT: subclasses MUST implement calculate_compensation(registry) and __str__()
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int) -> None:
        # Normalize and validate universal attributes
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
        # Digits-only storage; presentation formatting is an output concern
        return self._phone

    @phone.setter
    def phone(self, v: str) -> None:
        self._phone = self._normalize_phone(v)

    @staticmethod
    def _normalize_phone(v: str) -> str:
        # Keep only digits for canonical storage
        return "".join(ch for ch in str(v) if ch.isdigit())

    @property
    def years_of_service(self) -> int:
        # Tenure used by Staff compensation rule
        return max(0, CURRENT_YEAR - self.start_year)

    @abstractmethod
    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        # Each subclass must compute its own total compensation using the shared registry if needed.
        ...

    @abstractmethod
    def __str__(self) -> str:
        # Each subclass should provide a clean string for inclusion in reports.
        ...

    def compensation_summary(self, registry: ProjectRegistry) -> str:
        # Convenience method so the "print total compensation" can live in the class hierarchy.
        total = self.calculate_compensation(registry)
        return f"{self} | Total Compensation: ${total:,.2f}"


class GeneralManager(Employee):
    # GeneralManager has >= 1 projects; compensation is an equal share of 3% of TOTAL company project revenue.
    # DATA: inherits Employee fields; adds projects: List[Project]
    # COMP RULE: total_comp = (0.03 * sum(all unique project revenue)) / number_of_GMs
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 projects: List[Project]) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        if not projects:
            raise ValueError("GeneralManager must be associated with at least one project.")
        self._projects = list(projects)

    @property
    def projects(self) -> List[Project]:
        return list(self._projects)

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        pool = 0.03 * registry.total_revenue
        n = max(1, registry.gm_count)  # defensive split to avoid ZeroDivision if caller forgets to register GM
        return pool / n

    def __str__(self) -> str:
        pnames = ", ".join(p.name for p in self._projects)
        return f"[GM] {self.first_name} {self.last_name} (ID {self.emp_id}) | Projects: {pnames}"


class ProjectManager(Employee):
    # ProjectManager is assigned to EXACTLY one project; compensation is 5% of THAT project's revenue.
    # DATA: inherits Employee fields; adds project: Project
    # COMP RULE: total_comp = 0.05 * project.revenue
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


class Programmer(Employee):
    # Programmer is assigned to EXACTLY one project; compensation is base_salary + 1% of that project’s revenue.
    # DATA: inherits Employee fields; adds base_salary: float, project: Project
    # COMP RULE: total_comp = base_salary + 0.01 * project.revenue
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 base_salary: float, project: Project) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        self.base_salary = float(base_salary)  # use property for validation
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


class Staff(Employee):
    # Staff has no project; compensation is base_salary + $100 for each year of service.
    # DATA: inherits Employee fields; adds base_salary: float
    # COMP RULE: total_comp = base_salary + (100 * years_of_service)
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 base_salary: float) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        self.base_salary = float(base_salary)  # use property for validation

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

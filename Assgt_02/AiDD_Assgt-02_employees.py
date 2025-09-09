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


# ===========================================================================================
# Prompt to Copilot: Create a lightweight Project value-object with validation
# Goals:
#   - Define a frozen dataclass Project(name: str, revenue: float)
#   - Validate that name is non-empty and revenue is non-negative in __post_init__
#   - Implement __str__ to show a friendly representation "Project(name=..., revenue=...)".
# Constraints:
#   - Use @dataclass(frozen=True) so instances are immutable
#   - Keep logic minimal; heavy aggregates belong to ProjectRegistry
# ===========================================================================================
@dataclass(frozen=True)
class Project:
    """Value object representing a unique project and its revenue."""
    name: str
    revenue: float

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Project name cannot be empty.")
        if self.revenue < 0:
            raise ValueError("Project revenue cannot be negative.")

    def __str__(self) -> str:
        return f"Project(name={self.name}, revenue={self.revenue:,.2f})"


# ===========================================================================================
# Prompt to Copilot: Build ProjectRegistry to deduplicate projects and track GMs
# Goals:
#   - Maintain a dict of unique Project objects keyed by normalized name
#   - Expose upsert_project(name, revenue) with first-write-wins policy
#   - Provide get_project(name), total_revenue (sum of all unique), gm_count
#   - Track registered General Managers via register_gm(gm)
# Constraints:
#   - Normalize names via helper _key(name) -> lower/strip
#   - No global mutable state; this object is the single source of truth
# ===========================================================================================
class ProjectRegistry:
    """Central registry for unique projects and GM tracking."""
    def __init__(self) -> None:
        self._projects: Dict[str, Project] = {}
        self._general_managers: List["GeneralManager"] = []

    @staticmethod
    def _key(name: str) -> str:
        return name.strip().lower()

    def upsert_project(self, name: str, revenue: float) -> Project:
        """
        Insert-or-return an existing project by normalized name.
        First-write-wins for revenue (documented assumption).
        """
        k = self._key(name)
        if k in self._projects:
            return self._projects[k]
        proj = Project(name=name.strip(), revenue=float(revenue))
        self._projects[k] = proj
        return proj

    def get_project(self, name: str) -> Optional[Project]:
        """Return project by case-insensitive name, or None if absent."""
        return self._projects.get(self._key(name))

    def register_gm(self, gm: "GeneralManager") -> None:
        """Record GM for pool-splitting logic."""
        if gm not in self._general_managers:
            self._general_managers.append(gm)

    @property
    def total_revenue(self) -> float:
        """Aggregate revenue across all unique projects."""
        return sum(p.revenue for p in self._projects.values())

    @property
    def gm_count(self) -> int:
        """Number of registered General Managers."""
        return len(self._general_managers)


# ===========================================================================================
# Prompt to Copilot: Create the Parent Employee Class
# Based on the comments I provided, create the Employee parent class. It should:
#   - Import the datetime module at the top of the file (already done) and define CURRENT_YEAR.
#   - The __init__ method should accept first_name, last_name, emp_id, phone, and start_year.
#   - Normalize phone to digits only; validate names/ID are non-empty and start_year <= CURRENT_YEAR.
#   - Include a placeholder/abstract method calculate_compensation(registry) that child classes must implement.
#   - Include a placeholder/abstract __str__() method.
#   - Provide a years_of_service property and a helper compensation_summary(registry) that formats output.
# Constraints:
#   - Use ABC and @abstractmethod to enforce subclass overrides.
# ===========================================================================================
class Employee(ABC):
    """Superclass capturing universal identity/tenure logic and the polymorphic API."""
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
        """Digits-only phone; presentation formatting is an output concern."""
        return self._phone

    @phone.setter
    def phone(self, v: str) -> None:
        self._phone = self._normalize_phone(v)

    @staticmethod
    def _normalize_phone(v: str) -> str:
        """Strip non-digits to keep a canonical phone representation."""
        return "".join(ch for ch in str(v) if ch.isdigit())

    @property
    def years_of_service(self) -> int:
        """Compute tenure used by Staff compensation rule."""
        return max(0, CURRENT_YEAR - self.start_year)

    @abstractmethod
    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        """
        Polymorphic contract: subclasses must compute their total compensation
        using the shared registry where relevant.
        """
        ...

    @abstractmethod
    def __str__(self) -> str:
        """Polymorphic display for reports."""
        ...

    def compensation_summary(self, registry: ProjectRegistry) -> str:
        """Uniform printable string for compensation reports."""
        total = self.calculate_compensation(registry)
        return f"{self} | Total Compensation: ${total:,.2f}"


# ===========================================================================================
# Prompt to Copilot: Implement GeneralManager subclass
# Goals:
#   - Constructor must accept (first_name, last_name, emp_id, phone, start_year, projects: List[Project])
#   - Validate that projects list is non-empty
#   - calculate_compensation(registry): return equal share of 3% of registry.total_revenue across all GMs
#   - __str__() should include role tag, name/ID, and project names joined by comma
# Constraints:
#   - Use registry.gm_count defensively (treat 0 as 1 to avoid ZeroDivisionError)
# ===========================================================================================
class GeneralManager(Employee):
    """General Manager: ≥1 project; equal share of a 3% revenue pool across all GMs."""
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 projects: List[Project]) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        if not projects:
            raise ValueError("GeneralManager must be associated with at least one project.")
        self._projects = list(projects)

    @property
    def projects(self) -> List[Project]:
        """Defensive copy of associated projects."""
        return list(self._projects)

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        """GM pay = (0.03 * total unique project revenue) / number_of_GMs."""
        pool = 0.03 * registry.total_revenue
        n = max(1, registry.gm_count)
        return pool / n

    def __str__(self) -> str:
        pnames = ", ".join(p.name for p in self._projects)
        return f"[GM] {self.first_name} {self.last_name} (ID {self.emp_id}) | Projects: {pnames}"


# ===========================================================================================
# Prompt to Copilot: Implement ProjectManager subclass
# Goals:
#   - Constructor must accept (first_name, last_name, emp_id, phone, start_year, project: Project)
#   - calculate_compensation(registry): return 5% of that single project's revenue
#   - __str__() should include role tag, name/ID, and the project name
# Constraints:
#   - Exactly one project per PM
# ===========================================================================================
class ProjectManager(Employee):
    """Project Manager: exactly one project; 5% of that project's revenue."""
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 project: Project) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        self._project = project

    @property
    def project(self) -> Project:
        """The one project managed by this PM."""
        return self._project

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        """PM pay = 0.05 * project.revenue."""
        return 0.05 * self._project.revenue

    def __str__(self) -> str:
        return f"[PM] {self.first_name} {self.last_name} (ID {self.emp_id}) | Project: {self._project.name}"


# ===========================================================================================
# Prompt to Copilot: Implement Programmer subclass
# Goals:
#   - Constructor must accept (first_name, last_name, emp_id, phone, start_year, base_salary: float, project: Project)
#   - Validate base_salary >= 0 using a property setter
#   - calculate_compensation(registry): base_salary + 1% of that project's revenue
#   - __str__() shows role tag, name/ID, base salary, and project name
# Constraints:
#   - Exactly one project per Programmer
# ===========================================================================================
class Programmer(Employee):
    """Programmer: one project; base salary + 1% of that project's revenue."""
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 base_salary: float, project: Project) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        self.base_salary = float(base_salary)  # use property for validation
        self._project = project

    @property
    def base_salary(self) -> float:
        """Non-negative base salary with validation."""
        return self._base_salary

    @base_salary.setter
    def base_salary(self, v: float) -> None:
        v = float(v)
        if v < 0:
            raise ValueError("Base salary cannot be negative.")
        self._base_salary = v

    @property
    def project(self) -> Project:
        """The one project assigned to this programmer."""
        return self._project

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        """Programmer pay = base_salary + 0.01 * project.revenue."""
        return self._base_salary + 0.01 * self._project.revenue

    def __str__(self) -> str:
        return (f"[Programmer] {self.first_name} {self.last_name} (ID {self.emp_id}) | "
                f"Base ${self._base_salary:,.2f} | Project: {self._project.name}")


# ===========================================================================================
# Prompt to Copilot: Implement Staff subclass
# Goals:
#   - Constructor must accept (first_name, last_name, emp_id, phone, start_year, base_salary: float)
#   - Validate base_salary >= 0 using a property setter
#   - calculate_compensation(registry): base_salary + (100 * years_of_service)
#   - __str__() shows role tag, name/ID, and base salary
# Constraints:
#   - No project association for Staff
# ===========================================================================================
class Staff(Employee):
    """Staff: no project; base salary + $100 per year of service."""
    def __init__(self, first_name: str, last_name: str, emp_id: str, phone: str, start_year: int,
                 base_salary: float) -> None:
        super().__init__(first_name, last_name, emp_id, phone, start_year)
        self.base_salary = float(base_salary)  # use property for validation

    @property
    def base_salary(self) -> float:
        """Non-negative base salary with validation."""
        return self._base_salary

    @base_salary.setter
    def base_salary(self, v: float) -> None:
        v = float(v)
        if v < 0:
            raise ValueError("Base salary cannot be negative.")
        self._base_salary = v

    def calculate_compensation(self, registry: ProjectRegistry) -> float:
        """Staff pay = base_salary + (100 * years_of_service)."""
        return self._base_salary + (100.0 * self.years_of_service)

    def __str__(self) -> str:
        return f"[Staff] {self.first_name} {self.last_name} (ID {self.emp_id}) | Base ${self._base_salary:,.2f}"

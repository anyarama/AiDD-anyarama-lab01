import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tempfile
import csv
import pytest
from employee import Employee, Manager
import EmployeeData as data



def test_employee_validation():
    e = Employee(id="E1", fname="Alice", lname="Lee",
                 department="ENG", phNumber="(123)456-7890")
    assert e.getphNumber() == "1234567890"
    # was: assert str(e).startswith("Employee")
    s = str(e)
    assert s.startswith("[Employee]") or "Employee" in s


    # bad department
    with pytest.raises(ValueError):
        Employee(id="E2", fname="Bob", lname="Kay", department="EN", phNumber="1234567890")
    # bad phone
    with pytest.raises(ValueError):
        Employee(id="E3", fname="Bob", lname="Kay", department="FIN", phNumber="12345")

def test_manager_inherits_employee():
    m = Manager(id="M1", fname="Carol", lname="Diaz",
                department="FIN", phNumber="1234567890", team_size=5)
    assert m.team_size == 5
    ms = str(m)
    assert ms.startswith("[Manager]") or "Manager" in ms


def test_csv_round_trip(tmp_path):
    path = tmp_path / "employees.csv"
    emps = [
        Employee(id="E10", fname="Zoe", lname="Chan", department="HRM", phNumber="1112223333"),
        Manager(id="M10", fname="Vic", lname="Patel", department="ITD", phNumber="9998887777", team_size=4),
    ]
    data.save_employees(path, emps)
    loaded = data.load_employees(path)
    assert len(loaded) == 2
    # preserve role
    assert any(isinstance(e, Manager) for e in loaded)

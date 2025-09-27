const departmentSelect = document.getElementById("department");
const employeesBody = document.getElementById("employees-body");
const employeeRowTemplate = document.getElementById("employee-row");
const refreshButton = document.getElementById("refresh-btn");
const form = document.getElementById("employee-form");
const messageEl = document.getElementById("form-message");
const cancelEditButton = document.getElementById("cancel-edit");
const submitButton = form.querySelector("button[type='submit']");
const employeeCountEl = document.getElementById("employee-count");
const departmentCountEl = document.getElementById("department-count");
const avgSalaryEl = document.getElementById("avg-salary");
const departmentForm = document.getElementById("department-form");
const departmentInput = document.getElementById("new-department");
const departmentList = document.getElementById("department-list");
const departmentMessageEl = document.getElementById("department-message");

const API_BASE = ""; // same origin

let editingEmployeeId = null;
let cachedDepartments = [];

const formatCurrency = (salary) =>
  salary !== null && salary !== undefined && salary !== ""
    ? new Intl.NumberFormat(undefined, {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 2,
      }).format(Number(salary))
    : "—";

const formatDate = (value) => {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) {
    return value;
  }
  return date.toLocaleDateString();
};

async function fetchJSON(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

async function loadDepartments() {
  try {
    const departments = await fetchJSON("/api/departments");
    cachedDepartments = departments;
    departmentSelect.innerHTML = '<option value="">Select department</option>';
    departments.forEach(({ id, name }) => {
      const option = document.createElement("option");
      option.value = id;
      option.textContent = name;
      departmentSelect.appendChild(option);
    });
    if (departmentCountEl) {
      departmentCountEl.textContent = departments.length;
    }
    renderDepartments(departments);
  } catch (error) {
    console.error("Failed to load departments", error);
    cachedDepartments = [];
    if (departmentCountEl) {
      departmentCountEl.textContent = "0";
    }
    renderDepartments([]);
  }
}

function renderEmployees(employees) {
  employeesBody.innerHTML = "";

  if (!Array.isArray(employees) || employees.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 6;
    cell.classList.add("empty");
    cell.textContent = "No employees found.";
    row.appendChild(cell);
    employeesBody.appendChild(row);
    return;
  }

  employees.forEach((employee) => {
    const fragment = employeeRowTemplate.content.cloneNode(true);
    const row = fragment.querySelector("tr");
    row.dataset.id = employee.id;
    row.dataset.name = employee.name || "";
    row.dataset.departmentId = employee.department_id ?? "";
    row.dataset.salary = employee.salary ?? "";
    row.dataset.hireDate = employee.hire_date ?? "";
    fragment.querySelector(".col-id").textContent = employee.id;
    fragment.querySelector(".col-name").textContent = employee.name;
    fragment.querySelector(".col-department").textContent =
      employee.department_name || "—";
    fragment.querySelector(".col-salary").textContent = formatCurrency(
      employee.salary
    );
    fragment.querySelector(".col-hire-date").textContent = formatDate(
      employee.hire_date
    );
    employeesBody.appendChild(fragment);
  });
}

function renderDepartments(departments) {
  if (!departmentList) return;
  departmentList.innerHTML = "";

  if (!Array.isArray(departments) || departments.length === 0) {
    const emptyItem = document.createElement("li");
    emptyItem.className = "department-item empty";
    emptyItem.textContent = "No departments defined yet.";
    departmentList.appendChild(emptyItem);
    return;
  }

  departments.forEach((department) => {
    const item = document.createElement("li");
    item.className = "department-item";
    item.dataset.id = department.id;

    const nameSpan = document.createElement("span");
    nameSpan.className = "department-name";
    nameSpan.textContent = department.name;

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "chip-button danger";
    deleteButton.textContent = "Remove";

    item.appendChild(nameSpan);
    item.appendChild(deleteButton);
    departmentList.appendChild(item);
  });
}

function updateStats(employees) {
  const totalEmployees = Array.isArray(employees) ? employees.length : 0;
  if (employeeCountEl) {
    employeeCountEl.textContent = totalEmployees;
  }

  if (departmentCountEl && cachedDepartments.length) {
    departmentCountEl.textContent = cachedDepartments.length;
  }

  if (!avgSalaryEl) {
    return;
  }

  if (!totalEmployees) {
    avgSalaryEl.textContent = "—";
    return;
  }

  const salaries = (employees || [])
    .map((employee) =>
      employee.salary === null || employee.salary === undefined
        ? null
        : Number(employee.salary)
    )
    .filter((value) => typeof value === "number" && !Number.isNaN(value));

  if (!salaries.length) {
    avgSalaryEl.textContent = "—";
    return;
  }

  const average = salaries.reduce((total, value) => total + value, 0) / salaries.length;
  avgSalaryEl.textContent = formatCurrency(average);
}

async function loadEmployees() {
  try {
    const employees = await fetchJSON("/api/employees");
    renderEmployees(employees);
    updateStats(employees);
  } catch (error) {
    console.error("Failed to load employees", error);
    renderEmployees([]);
    updateStats([]);
  }
}

function setFormMessage(text, type = "") {
  messageEl.textContent = text;
  messageEl.className = type ? type : "";
}

function setDepartmentMessage(text, type = "") {
  if (!departmentMessageEl) return;
  departmentMessageEl.textContent = text;
  departmentMessageEl.className = type ? type : "";
}

function resetForm() {
  form.reset();
  editingEmployeeId = null;
  submitButton.textContent = "Add Employee";
  cancelEditButton.hidden = true;
  form.classList.remove("is-editing");
}

function beginEdit(row) {
  editingEmployeeId = row.dataset.id;
  form.name.value = row.dataset.name || "";
  departmentSelect.value = row.dataset.departmentId || "";
  form.salary.value = row.dataset.salary || "";
  form["hire-date"].value = row.dataset.hireDate || "";
  submitButton.textContent = "Update Employee";
  cancelEditButton.hidden = false;
  form.classList.add("is-editing");
  setFormMessage(`Editing employee #${editingEmployeeId}`, "info");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setFormMessage("", "");

  const formData = new FormData(form);
  const payload = {
    name: formData.get("name"),
    department_id: formData.get("department") || null,
    salary: formData.get("salary") || null,
    hire_date: formData.get("hire-date") || null,
  };

  // coerce empty values to null
  if (!payload.department_id) {
    payload.department_id = null;
  }
  if (!payload.salary) {
    payload.salary = null;
  }
  if (!payload.hire_date) {
    payload.hire_date = null;
  }

  try {
    submitButton.disabled = true;
    if (editingEmployeeId) {
      await fetchJSON(`/api/employees/${editingEmployeeId}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      setFormMessage("Employee updated successfully!", "success");
    } else {
      await fetchJSON("/api/employees", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setFormMessage("Employee added successfully!", "success");
    }
    resetForm();
    await loadEmployees();
  } catch (error) {
    const action = editingEmployeeId ? "Update" : "Add";
    console.error(`${action} employee failed`, error);
    const message = error.message.replace(/^\"|\"$/g, "");
    setFormMessage(message || `Unable to ${action.toLowerCase()} employee.`, "error");
  } finally {
    submitButton.disabled = false;
  }
});

employeesBody.addEventListener("click", async (event) => {
  const target = event.target;
  const row = target.closest("tr");
  if (!row) return;

  if (target.classList.contains("delete-btn")) {
    const employeeId = row.dataset.id;
    if (!employeeId) return;

    const confirmed = window.confirm(
      "Are you sure you want to delete this employee?"
    );
    if (!confirmed) {
      return;
    }

    try {
      await fetchJSON(`/api/employees/${employeeId}`, { method: "DELETE" });
      row.remove();
      await loadEmployees();
      if (editingEmployeeId === employeeId) {
        resetForm();
      }
      setFormMessage("Employee deleted.", "success");
    } catch (error) {
      console.error("Delete failed", error);
      alert("Failed to delete employee. Check console for details.");
    }
    return;
  }

  if (target.classList.contains("edit-btn")) {
    beginEdit(row);
    return;
  }
});

refreshButton.addEventListener("click", () => {
  loadEmployees();
});

cancelEditButton.addEventListener("click", () => {
  resetForm();
  setFormMessage("Edit cancelled.", "info");
});

if (departmentForm) {
  departmentForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!departmentInput) return;

    const name = departmentInput.value.trim();
    if (!name) {
      setDepartmentMessage("Please enter a department name.", "error");
      return;
    }

    try {
      departmentForm.querySelector("button[type='submit']").disabled = true;
      await fetchJSON("/api/departments", {
        method: "POST",
        body: JSON.stringify({ name }),
      });
      departmentInput.value = "";
      setDepartmentMessage("Department added.", "success");
      await loadDepartments();
    } catch (error) {
      console.error("Add department failed", error);
      const message = error.message.replace(/^\"|\"$/g, "");
      setDepartmentMessage(message || "Unable to add department.", "error");
    } finally {
      departmentForm.querySelector("button[type='submit']").disabled = false;
    }
  });
}

if (departmentList) {
  departmentList.addEventListener("click", async (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;

    if (!target.classList.contains("chip-button")) {
      return;
    }

    const item = target.closest("li");
    const id = item?.dataset.id;
    if (!id) return;

    const confirmed = window.confirm("Remove this department?");
    if (!confirmed) return;

    try {
      target.disabled = true;
      await fetchJSON(`/api/departments/${id}`, { method: "DELETE" });
      setDepartmentMessage("Department removed.", "success");
      await loadDepartments();
    } catch (error) {
      console.error("Delete department failed", error);
      const message = error.message.replace(/^\"|\"$/g, "");
      setDepartmentMessage(message || "Unable to remove department.", "error");
      target.disabled = false;
    }
  });
}

(async function init() {
  await loadDepartments();
  await loadEmployees();
})();

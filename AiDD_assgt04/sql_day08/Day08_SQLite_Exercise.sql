-- Day08_SQLite_Exercise.sql
-- Company DB DDL + DML + Query Ops
-- Run with: sqlite3 company_db.sqlite < Day08_SQLite_Exercise.sql


--Project: AiDD-anyarama-lab01/AiDD_assgt04
--By: Aneesh Yaramati, Shamik Dutta Majumdar


PRAGMA foreign_keys = ON;

-- 1) Create schema
DROP TABLE IF EXISTS employee_projects;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
  department_id   INTEGER PRIMARY KEY,
  department_name TEXT NOT NULL UNIQUE
);

CREATE TABLE employees (
  employee_id   INTEGER PRIMARY KEY,
  first_name    TEXT NOT NULL,
  last_name     TEXT NOT NULL,
  email         TEXT UNIQUE,
  hire_date     DATE NOT NULL,
  department_id INTEGER NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments(department_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE projects (
  project_id   INTEGER PRIMARY KEY,
  project_name TEXT NOT NULL UNIQUE,
  start_date   DATE,
  end_date     DATE
);

CREATE TABLE employee_projects (
  employee_id INTEGER NOT NULL,
  project_id  INTEGER NOT NULL,
  PRIMARY KEY (employee_id, project_id),
  FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
  FOREIGN KEY (project_id)  REFERENCES projects(project_id)  ON DELETE CASCADE
);

CREATE TABLE tasks (
  task_id     INTEGER PRIMARY KEY,
  task_name   TEXT NOT NULL,
  project_id  INTEGER NOT NULL,
  employee_id INTEGER,
  FOREIGN KEY (project_id)  REFERENCES projects(project_id)  ON DELETE CASCADE,
  FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

-- 2) Seed data
INSERT INTO departments(department_id, department_name) VALUES
  (10, 'HR'),
  (20, 'ENG'),
  (30, 'FIN');

INSERT INTO employees(employee_id, first_name, last_name, email, hire_date, department_id) VALUES
  (1, 'Alicia', 'Lee', 'alicia.lee@example.com', '2023-06-01', 20),
  (2, 'Bharat', 'Patel', 'bharat.patel@example.com', '2022-02-15', 20),
  (3, 'Carla', 'Mendez', 'carla.mendez@example.com', '2021-09-20', 10),
  (4, 'Diego', 'Santos', 'diego.santos@example.com', '2024-01-10', 30);

INSERT INTO projects(project_id, project_name, start_date, end_date) VALUES
  (100, 'Data Lake Revamp', '2024-02-01', NULL),
  (200, 'Payroll Cleanup',  '2024-03-10', '2024-08-31');

INSERT INTO employee_projects(employee_id, project_id) VALUES
  (1, 100),
  (2, 100),
  (3, 200),
  (4, 200);

INSERT INTO tasks(task_name, project_id, employee_id) VALUES
  ('Build ingestion pipelines', 100, 1),
  ('Optimize Spark jobs',       100, 2),
  ('Audit pay codes',           200, 3),
  ('Automate GL export',        200, 4);

-- 3) Required operations

-- 3.1 Retrieve all employees and their associated projects.
SELECT e.employee_id, e.first_name, e.last_name, p.project_id, p.project_name
FROM employees e
LEFT JOIN employee_projects ep ON ep.employee_id = e.employee_id
LEFT JOIN projects p           ON p.project_id    = ep.project_id
ORDER BY e.employee_id, p.project_id;

-- 3.2 Find employees who belong to a specific department (parameterized example with dept id 20).
SELECT e.employee_id, e.first_name, e.last_name, d.department_name
FROM employees e
JOIN departments d ON d.department_id = e.department_id
WHERE e.department_id = 20
ORDER BY e.employee_id;

-- 3.3 List all projects and the employees working on each project.
SELECT p.project_id, p.project_name, e.employee_id, e.first_name, e.last_name
FROM projects p
LEFT JOIN employee_projects ep ON ep.project_id = p.project_id
LEFT JOIN employees e          ON e.employee_id = ep.employee_id
ORDER BY p.project_id, e.employee_id;

-- 3.4 Update the task assigned to an employee on a specific project.
-- Example: reassign 'Optimize Spark jobs' on project 100 from employee 2 to employee 1
UPDATE tasks
SET employee_id = 1
WHERE task_name = 'Optimize Spark jobs' AND project_id = 100;

-- Verify
SELECT task_id, task_name, project_id, employee_id FROM tasks WHERE project_id = 100;

-- 3.5 Delete a project and remove associated tasks and employee_project records.
-- Example: delete project 200
DELETE FROM projects WHERE project_id = 200;

-- Verify cascades
SELECT * FROM projects;
SELECT * FROM tasks;
SELECT * FROM employee_projects;

-- 4) Two additional exploratory queries

-- 4.1 Count of employees per department with names
SELECT d.department_name, COUNT(e.employee_id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.department_id = d.department_id
GROUP BY d.department_id
ORDER BY headcount DESC;

-- 4.2 Projects without assigned employees (after deletion above)
SELECT p.project_id, p.project_name
FROM projects p
LEFT JOIN employee_projects ep ON ep.project_id = p.project_id
WHERE ep.employee_id IS NULL;


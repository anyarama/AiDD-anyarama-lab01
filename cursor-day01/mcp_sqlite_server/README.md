# SQLite MCP Server

This folder contains a minimal Model Context Protocol server that exposes controlled
access to the `employees.db` SQLite database in the repository root. The
server is designed so that you can add it as a custom MCP server in Cursor and
then let Cursor's AI run queries against the database without direct file
access.

## Prerequisites

- Python 3.9 or later available on your PATH
- The `mcp` Python package (install with `pip install -r requirements.txt`)
- The `employees.db` SQLite file living one directory above this folder (already
  present in the repo)

## Quick start

1. Create and activate a virtual environment (optional but recommended):
   ```bash
   cd /Users/aneeshyaramati/Documents/GitHub/AiDD-anyarama-lab01/cursor-day01/mcp_sqlite_server
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Run the server manually to make sure it starts without errors:
   ```bash
   python sqlite_server.py
   ```
   The process will wait for MCP messages on stdin/stdout. Use `Ctrl+C` to stop
   it.

## Registering the server in Cursor

1. Open Cursor ➜ Settings ➜ MCP Servers ➜ "Add Server".
2. Choose "Manifest file" and point Cursor to the `manifest.json` in this
   directory (see below for the format).
3. Cursor will use the manifest to start the Python script and connect via MCP.
4. In a chat, you can now ask Cursor to run the `run_sql` tool, for example:
   "Use run_sql to list the first 5 employees". To add staff, invoke the
   `add_employee` tool with the required fields (see below).

## Manifest

Cursor expects a manifest describing how to launch the server. Place the
following JSON in `mcp_sqlite_server/manifest.json`:

```json
{
  "name": "sqlite-mcp-server",
  "description": "SQLite access to employees.db",
  "entrypoint": {
    "command": "python",
    "args": [
      "sqlite_server.py"
    ],
    "cwd": "."
  }
}
```

When Cursor loads this manifest it will start the process with the working
directory set to the folder so the relative path to `employees.db` resolves.

## Tool behavior

- `run_sql`
  - `query` (string, required): SQL statement that must start with `SELECT`.
  - `parameters` (array of strings or numbers, optional): bound parameters for
    `?` placeholders in the query.
  - Returns JSON text representing the selected rows.
- `add_employee`
  - `name` (string, required): employee name.
  - `department_id` (integer, optional): department foreign key.
  - `salary` (number, optional): employee salary.
  - `hire_date` (string, optional): date string such as `2024-01-31`.
  - Returns the inserted row (including the generated id) as JSON text.

All writes are limited to inserting new employees; extend the server if you need
additional operations.

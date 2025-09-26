"""Simple MCP server exposing controlled access to employees.db."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import anyio
import mcp
from mcp import types
from mcp.server import Server

# Derive the database path relative to the repository root.
DB_PATH = Path(__file__).resolve().parent.parent / "employees.db"

# The server name is what Cursor will show to you.
server = Server("sqlite-mcp-server")


def _rows_to_json(cursor: sqlite3.Cursor) -> str:
    """Format sqlite rows as a JSON string."""
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return json.dumps(rows, indent=2)


@server.list_tools()
async def list_tools(_request: types.ListToolsRequest) -> types.ListToolsResult:
    """Expose database utilities to the MCP client."""
    return types.ListToolsResult(
        tools=[
            types.Tool(
                name="run_sql",
                description=(
                    "Execute a read-only SQL query against employees.db. "
                    "Accepts SELECT statements only."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL SELECT statement to execute.",
                        },
                        "parameters": {
                            "type": "array",
                            "items": {
                                "type": ["string", "number"],
                            },
                            "description": (
                                "Optional positional parameters to bind using "
                                "SQLite's ? placeholders. Strings and numbers "
                                "are supported."
                            ),
                            "default": [],
                        },
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="add_employee",
                description=(
                    "Insert a new employee row into the database. "
                    "Requires at least the employee name."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Full name of the employee.",
                        },
                        "department_id": {
                            "type": ["integer", "null"],
                            "description": "Department foreign key (optional).",
                        },
                        "salary": {
                            "type": ["number", "null"],
                            "description": "Annual salary for the employee.",
                        },
                        "hire_date": {
                            "type": ["string", "null"],
                            "description": "Hire date, e.g. 2024-01-31.",
                        },
                    },
                    "required": ["name"],
                },
            ),
        ]
    )


def _ensure_database_present() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found at {DB_PATH!s}")


def _handle_run_sql(arguments: dict[str, Any]) -> list[types.TextContent]:
    query = arguments.get("query")
    if not isinstance(query, str):
        raise ValueError("`query` must be provided as a string.")

    lowered = query.strip().lower()
    if not lowered.startswith("select"):
        raise ValueError("Only SELECT statements are permitted for run_sql.")

    parameters = arguments.get("parameters", [])
    if parameters is None:
        parameters = []
    if not isinstance(parameters, list) or not all(
        isinstance(item, (str, int, float)) for item in parameters
    ):
        raise ValueError(
            "`parameters` must be a list containing strings, integers, or floats."
        )

    _ensure_database_present()

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(query, tuple(parameters))
            payload = _rows_to_json(cursor)
    except sqlite3.Error as exc:
        raise ValueError(f"SQLite error: {exc}") from exc

    return [types.TextContent(type="text", text=payload)]


def _handle_add_employee(arguments: dict[str, Any]) -> list[types.TextContent]:
    name = arguments.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("`name` must be a non-empty string.")

    department_id = arguments.get("department_id")
    if department_id is not None and not isinstance(department_id, int):
        raise ValueError("`department_id` must be an integer when provided.")

    salary = arguments.get("salary")
    if salary is not None:
        if isinstance(salary, (int, float)):
            salary = float(salary)
        else:
            raise ValueError("`salary` must be numeric when provided.")

    hire_date = arguments.get("hire_date")
    if hire_date is not None:
        if not isinstance(hire_date, str) or not hire_date.strip():
            raise ValueError("`hire_date` must be a non-empty string when provided.")
        hire_date = hire_date.strip()

    columns = ["name"]
    values: list[Any] = [name.strip()]
    placeholders = ["?"]

    if department_id is not None:
        columns.append("department_id")
        values.append(department_id)
        placeholders.append("?")

    if salary is not None:
        columns.append("salary")
        values.append(salary)
        placeholders.append("?")

    if hire_date is not None:
        columns.append("hire_date")
        values.append(hire_date)
        placeholders.append("?")

    insert_sql = (
        f"INSERT INTO employees ({', '.join(columns)}) "
        f"VALUES ({', '.join(placeholders)})"
    )

    _ensure_database_present()

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(insert_sql, tuple(values))
            employee_id = cursor.lastrowid
            result_cursor = conn.execute(
                "SELECT id, name, department_id, salary, hire_date FROM employees WHERE id = ?",
                (employee_id,),
            )
            payload = _rows_to_json(result_cursor)
    except sqlite3.Error as exc:
        raise ValueError(f"SQLite error: {exc}") from exc

    return [
        types.TextContent(
            type="text",
            text=payload,
        )
    ]


@server.call_tool()
async def handle_tool(tool_name: str, arguments: dict[str, Any]):
    """Dispatch tools based on the requested name."""
    if tool_name == "run_sql":
        return _handle_run_sql(arguments)
    if tool_name == "add_employee":
        return _handle_add_employee(arguments)
    raise ValueError(f"Unsupported tool: {tool_name}")


async def _serve() -> None:
    initialization_options = server.create_initialization_options()
    async with mcp.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, initialization_options)


def main() -> None:
    """Entrypoint used by the MCP runtime."""
    anyio.run(_serve)


if __name__ == "__main__":
    main()

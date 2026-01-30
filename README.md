# Easy Jupyter Editor MCP

A lightweight Model Context Protocol (MCP) server designed to allow AI Agents to safely and structurally edit Jupyter Notebook (`.ipynb`) files.

## Background

This MCP server was developed to enable **AI agents to safely manipulate Jupyter Notebook (.ipynb) files**.

In many AI agent environments (such as Antigravity), directly executing notebook files or editing complex `.ipynb` JSON structures as raw text can be difficult due to security restrictions or the risk of corrupting the file format.

This project aims to **"structurally edit Notebook files correctly while bypassing execution permission issues."** By using the `nbformat` library, it allows adding, editing, and deleting cells without breaking the JSON structure.

## Features

Provides the following tools:
*   **`read_notebook`**: Retrieves a list of cells (index and content summary) from a Notebook.
*   **`get_cell`**: Retrieves the full source code of a specific cell by index.
*   **`edit_cell`**: Modifies the content of a specific cell.
*   **`add_cell`**: Adds a new code or Markdown cell.
*   **`delete_cell`**: Deletes a specific cell.
*   **`create_notebook`**: Creates a new, empty Notebook.

## Installation & Usage

It is recommended to run this server using [uv](https://github.com/astral-sh/uv).

### 1. Claude Desktop / MCP Client Configuration

Add the following configuration to `claude_desktop_config.json`.

#### Running directly from GitHub (Recommended)
```json
{
  "mcpServers": {
    "easy-jupyter-editor": {
      "command": "uv",
      "args": [
        "run",
        "--from",
        "git+https://github.com/YourUsername/easy-jupyter-editor-mcp",
        "easy-jupyter-editor-mcp"
      ]
    }
  }
}
```

#### Running Locally for Development
```json
{
  "mcpServers": {
    "easy-jupyter-editor": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "nbformat",
        "python",
        "/absolute/path/to/easy-jupyter-editor-mcp/src/easy_jupyter_editor_mcp/__init__.py"
      ]
    }
  }
}
```

### 2. PyPI (Future Publication)

If published to PyPI, you can configure it simply as:

```json
{
  "mcpServers": {
    "easy-jupyter-editor": {
      "command": "uvx",
      "args": ["easy-jupyter-editor-mcp"]
    }
  }
}
```

## Development

```bash
# Build
uv build

# Publish to PyPI
uv publish
```

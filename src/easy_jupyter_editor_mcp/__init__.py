import nbformat
import os
from mcp.server.fastmcp import FastMCP
from typing import List, Optional

# Initialize the MCP Server
mcp = FastMCP("Jupyter Notebook Editor")

def _load_notebook(path: str) -> nbformat.NotebookNode:
    """Helper to load a notebook from disk."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Notebook not found at: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        # as_version=4 ensures we get a standard node structure
        return nbformat.read(f, as_version=4)

def _save_notebook(path: str, nb: nbformat.NotebookNode):
    """Helper to save a notebook to disk."""
    with open(path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

@mcp.tool()
def read_notebook(path: str) -> str:
    """
    Reads a Jupyter Notebook and returns a summary of its cells.
    Use this to identify cell indices before editing.
    
    Args:
        path: Absolute path to the .ipynb file.
        
    Returns:
        Formatted string showing index, type, and truncated content of each cell.
    """
    try:
        nb = _load_notebook(path)
        result = [f"Notebook: {os.path.basename(path)} ({len(nb.cells)} cells)\n"]
        
        for i, cell in enumerate(nb.cells):
            cell_type = cell.cell_type.upper()
            source = cell.source.strip()
            # Truncate long content for readability
            preview = source[:100].replace('\n', '\\n') + "..." if len(source) > 100 else source.replace('\n', '\\n')
            result.append(f"[{i}] [{cell_type}]: {preview}")
            
        return "\n".join(result)
    except Exception as e:
        return f"Error reading notebook: {str(e)}"

@mcp.tool()
def get_cell(path: str, index: int) -> str:
    """
    Gets the full content of a specific cell.
    
    Args:
        path: Absolute path to the .ipynb file.
        index: The index of the cell (0-based).
        
    Returns:
        The full source code of the cell.
    """
    try:
        nb = _load_notebook(path)
        if index < 0 or index >= len(nb.cells):
            return f"Error: Index {index} is out of bounds (0-{len(nb.cells)-1})."
            
        return nb.cells[index].source
    except Exception as e:
        return f"Error getting cell: {str(e)}"

@mcp.tool()
def edit_cell(path: str, index: int, source: str) -> str:
    """
    Edits the source code of an existing cell.
    
    Args:
        path: Absolute path to the .ipynb file.
        index: The index of the cell to modify.
        source: The new source code for the cell.
        
    Returns:
        Success message.
    """
    try:
        nb = _load_notebook(path)
        if index < 0 or index >= len(nb.cells):
            return f"Error: Index {index} is out of bounds (0-{len(nb.cells)-1})."
            
        nb.cells[index].source = source
        _save_notebook(path, nb)
        return f"Successfully updated cell {index}."
    except Exception as e:
        return f"Error editing cell: {str(e)}"

@mcp.tool()
def add_cell(path: str, source: str, cell_type: str = "code", index: int = -1) -> str:
    """
    Adds a new cell to the notebook.
    
    Args:
        path: Absolute path to the .ipynb file.
        source: The source code/text for the new cell.
        cell_type: "code" or "markdown".
        index: Integration position. -1 appends to the end.
        
    Returns:
        Success message with the new cell's index.
    """
    try:
        nb = _load_notebook(path)
        
        if cell_type.lower() == "code":
            new_cell = nbformat.v4.new_code_cell(source)
        elif cell_type.lower() == "markdown":
            new_cell = nbformat.v4.new_markdown_cell(source)
        else:
            return f"Error: Unsupported cell type '{cell_type}'. Use 'code' or 'markdown'."
            
        if index == -1 or index >= len(nb.cells):
            nb.cells.append(new_cell)
            new_index = len(nb.cells) - 1
        else:
            nb.cells.insert(index, new_cell)
            new_index = index
            
        _save_notebook(path, nb)
        return f"Successfully added {cell_type} cell at index {new_index}."
    except Exception as e:
        return f"Error adding cell: {str(e)}"

@mcp.tool()
def delete_cell(path: str, index: int) -> str:
    """
    Deletes a cell from the notebook.
    
    Args:
        path: Absolute path to the .ipynb file.
        index: The index of the cell to delete.
        
    Returns:
        Success message.
    """
    try:
        nb = _load_notebook(path)
        if index < 0 or index >= len(nb.cells):
            return f"Error: Index {index} is out of bounds (0-{len(nb.cells)-1})."
            
        deleted_type = nb.cells[index].cell_type
        del nb.cells[index]
        _save_notebook(path, nb)
        return f"Successfully deleted {deleted_type} cell at index {index}."
    except Exception as e:
        return f"Error deleting cell: {str(e)}"

@mcp.tool()
def create_notebook(path: str) -> str:
    """
    Creates a new, empty Jupyter Notebook.
    
    Args:
        path: Absolute path where the .ipynb file should be created.
        
    Returns:
        Success message.
    """
    try:
        if os.path.exists(path):
            return f"Error: File already exists at {path}"
            
        nb = nbformat.v4.new_notebook()
        _save_notebook(path, nb)
        return f"Successfully created new notebook at {path}"
    except Exception as e:
        return f"Error creating notebook: {str(e)}"


def main():
    mcp.run()

if __name__ == "__main__":
    main()

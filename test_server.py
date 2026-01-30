import os
import nbformat
from server import read_notebook, add_cell, edit_cell, delete_cell, create_notebook, get_cell

TEST_NB = "test_notebook.ipynb"

def run_tests():
    print("--- Starting Verification ---")
    
    # 0. Clean up
    if os.path.exists(TEST_NB):
        os.remove(TEST_NB)
        
    # 1. Create Notebook
    print(f"Creating {TEST_NB}...")
    res = create_notebook(os.path.abspath(TEST_NB))
    print(res)
    assert "Successfully created" in res

    # 2. Add Cells
    print("Adding cells...")
    add_cell(os.path.abspath(TEST_NB), "print('Hello World')", "code")
    add_cell(os.path.abspath(TEST_NB), "# My Title", "markdown", 0) # Insert at top
    
    # 3. Read Notebook
    print("Reading notebook...")
    content = read_notebook(os.path.abspath(TEST_NB))
    print(content)
    assert "# My Title" in content
    assert "print('Hello World')" in content
    
    # 4. Edit Cell
    print("Editing cell 1...")
    edit_cell(os.path.abspath(TEST_NB), 1, "print('Edited World')")
    new_content = get_cell(os.path.abspath(TEST_NB), 1)
    print(f"New content of cell 1: {new_content}")
    assert "Edited World" in new_content
    
    # 5. Delete Cell
    print("Deleting cell 0...")
    delete_cell(os.path.abspath(TEST_NB), 0)
    final_content = read_notebook(os.path.abspath(TEST_NB))
    print("Final content summary:")
    print(final_content)
    assert "# My Title" not in final_content # Should be gone
    
    print("\n--- PASSED ALL TESTS ---")

if __name__ == "__main__":
    run_tests()

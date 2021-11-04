from library.jupyter_notebook_lib import *
from library.jupyter_jsonfiles_lib import *

source_path = "../examples"
source_file = "input_files/pandas_examples.ipynb"
destination_file = "output_files/pandas_toc.txt"


input_notebook_path = source_path + "/" + source_file
output_python_path = source_path + "/" + destination_file

input_notebook_json = read_json_file(input_notebook_path)

nb = JupyterNotebook()
nb.load_from_json(input_notebook_json)

nb.clear_cells_output()
nb.remove_empty_cells()

toc_cell, extracted_python_titles = nb.get_notebook_table_of_content()

with open(output_python_path, "w") as file:
    file.writelines("\n".join(extracted_python_titles))

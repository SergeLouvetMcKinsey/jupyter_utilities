from library.jupyter_notebook_lib import *
from library.jupyter_jsonfiles_lib import *


source_path = "../examples"
source_file = "input_files/pandas_examples.ipynb"
destination_file = "output_files/pandas_test.py"

input_notebook_path = source_path + "/" + source_file
output_python_path = source_path + "/" + destination_file

input_notebook_json = read_json_file(input_notebook_path)

nb = JupyterNotebook()
nb.load_from_json(input_notebook_json)

nb.clear_cells_output()
nb.remove_empty_cells()

lines_to_comment = ["!pip install pandas","!pip install openpyxl"]
data_path_resolution = {}

extracted_python_code = nb.get_notebook_source(lines_to_comment, data_path_resolution, True)

with open(output_python_path, "w") as file:
    file.writelines("\n".join(extracted_python_code))

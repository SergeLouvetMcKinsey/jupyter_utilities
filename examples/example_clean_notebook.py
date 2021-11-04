from library.jupyter_notebook_lib import *
from library.jupyter_jsonfiles_lib import *

source_path = "../examples"
source_file = "input_files/pandas_examples.ipynb"
destination_file = "output_files/pandas_examples.ipynb"

input_notebook_path = source_path + "/" + source_file
output_notebook_path = source_path + "/" + destination_file

input_notebook_json = read_json_file(input_notebook_path)

nb = JupyterNotebook()
nb.load_from_json(input_notebook_json)

nb.clear_cells_output()
nb.remove_empty_cells()

output_notebook_json = nb.get_json_dict()
write_json_file(output_notebook_json, output_notebook_path)


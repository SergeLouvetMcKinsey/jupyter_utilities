from shutil import copy2

from jupyter_notebook_lib import *
from jupyter_jsonfiles_lib import *

source_path = "C:/Users/Serge Louvet/Box Sync/LittleFolder/Projects/2021/B2B_DataEngineering/dev/pandas_cheat_code"
source_file = "pandas_cheat_code.ipynb"
destination_file = "pandas_test.py"

input_notebook_path = source_path + "/" + source_file
output_python_path = source_path + "/" + destination_file

input_notebook_json = read_json_file(input_notebook_path)

nb = JupyterNotebook()
nb.load_from_json(input_notebook_json)

nb.clear_cells_output()
nb.remove_empty_cells()

extracted_python_code = nb.get_notebook_source([], {}, True)

with open(output_python_path, "w") as file:
    file.writelines("\n".join(extracted_python_code))

import json
from shutil import copy2
import datetime
import time

MY_VERSION = "1.0"


def extract_code_from_jupyter_json(
        notebook_json,
        data_path_resolution,
        lines_to_comment,
        trace_print_cells = True
):
    """
    Args:
        notebook_json: json object from the jupyter notebook
        data_path_resolution: dictionary of variable containing datapath, to be updated during codde extraction
    """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    source_list = [
        "#",
        f"# Jupyter Notebook conversion utility version {MY_VERSION}",
        f"# Converted on {st}",
        "#",
    ]

    list_of_cells = notebook_json["cells"]

    cell_counter = 0
    for cell in list_of_cells:
        cell_counter += 1
        cell_type = cell["cell_type"]
        cell_source_list = []
        has_import = False
        if cell_type == "code":
            cell_source = cell["source"]
            cell_source_list.append(f"# Cell {cell_counter}")

            for source_line in cell_source:
                source_line = source_line.replace("\n", "")

                has_import = has_import or source_line.strip()[0:7] == "import " or source_line.strip()[0:5] == "from "

                if source_line.strip() in lines_to_comment:
                    source_line = "# " + source_line

                for k, v in data_path_resolution.items():
                    if (
                        k == source_line.strip()[0 : len(k)]
                        and source_line.find("=") > 1
                        and source_line.find(",") < 0
                    ):

                        print(k, source_line)
                        pos_equal = source_line.find("=")
                        source_line = source_line[0 : pos_equal + 1] + ' "' + v + '"'
                        print(k, source_line)
                cell_source_list.append(source_line)

            if trace_print_cells and not has_import:
                source_list.append("")
                source_list.append(f"print(\"Cell {cell_counter}\")")
                source_list.append("")

            for line in cell_source_list:
                source_list.append(line)

    return source_list


def extract_code_from_jupyter_notebook(
    notebook_path, data_path_resolution, lines_to_comment, python_script_path
):
    with open(notebook_path) as file:
        notebook_source = file.readlines()

    notebook_json = json.loads("\n".join(notebook_source))

    extracted_python_code = extract_code_from_jupyter_json(
        notebook_json, data_path_resolution, lines_to_comment
        )

    tmp_python_output  = python_script_path

    with open(tmp_python_output, "w") as file:
        file.writelines("\n".join(extracted_python_code))


def clean_jupyter_json(
    notebook_json, clear_code_output=False, remove_empty_cells=False
):
    """
    Clean a jupyter notebook
    Remove empty cells (if remove_empty_cells flag it True)
    Clear output from code cells (if clear_code_output flag is True)

    Args:
        notebook_json: json object from the jupyter notebook
        clear_code_output: clear code output if True
        remove_empty_cells: remove empty cells (any type) if True

    Returns:
        A dictionary with counters:
            nb_cells: number of cells processed
            nb_code_cells: number of code cells processed
            nb_empty_cells: number of empty cells removed
            nb_clear_output: number of code cells of which output has been cleared

    """
    list_of_cells = notebook_json["cells"]

    nb_cells = 0
    nb_code_cells = 0
    nb_clear_output = 0
    nb_empty_cells = 0

    output_cells = []
    for cell in list_of_cells:
        nb_cells += 1
        cell_type = cell["cell_type"]
        if cell_type == "code":
            nb_code_cells += 1
            cell_output = cell["outputs"]
            if len(cell_output) > 0:
                nb_clear_output += 1

                if clear_code_output:
                    cell["outputs"] = []

        if len(cell["source"]) == 0:
            nb_empty_cells += 1
            if not remove_empty_cells:
                output_cells.append(cell)
        else:
            output_cells.append(cell)

    notebook_json["cells"] = output_cells

    return {
        "nb_cells": nb_cells,
        "nb_code_cells": nb_code_cells,
        "nb_clear_output": nb_clear_output,
        "nb_empty_cells": nb_empty_cells,
    }


def clean_jupyter_notebook(
    notebook_path, clear_output=False, remove_empty_cells=False, new_notebook_path=""
):
    """
    Clean a jupyter notebook
    Remove empty cells (if remove_empty_cells flag it True)
    Clear output from code cells (if clear_code_output flag is True)

    Args:
        notebook_path: path to the jupyter notebook source file
        clear_code_output: clear code output if True
        remove_empty_cells: remove empty cells (any type) if True
        new_notebook_path: optional path for the updated notebook
            if empty, the update notebook replaces the source notebook, after creating a backup copy

    Returns:
        A dictionary with counters:
            nb_cells: number of cells processed
            nb_code_cells: number of code cells processed
            nb_empty_cells: number of empty cells removed
            nb_clear_output: number of code cells of which output has been cleared
            input: path to source jupyter notebook
            backup: path to backed up jupyter notebook
            output: path to updated jupyter notebook

    """

    with open(notebook_path) as file:
        notebook_source = file.readlines()

    notebook_json = json.loads("\n".join(notebook_source))

    return_element = clean_jupyter_json(notebook_json, clear_output, remove_empty_cells)

    if len(new_notebook_path) == 0:
        output_path = notebook_path
        copy2(notebook_path, notebook_path + ".bak")
        return_element["input"] = notebook_path
        return_element["backup"] = notebook_path + ".bak"
        return_element["output"] = notebook_path
    else:
        output_path = new_notebook_path
        return_element["input"] = notebook_path
        return_element["backup"] = ""
        return_element["output"] = new_notebook_path

    with open(output_path, "w") as file:
        file.writelines(json.dumps(notebook_json, indent=3))

    return return_element


ipynb_input = "Cortex-data-library/cortex_data_library/docs/source/examples/end_to_end_example_01.ipynb"
ipynb_output = "Cortex-data-library/cortex_data_library/docs/source/examples/end_to_end_example_03.ipynb"
python_output = "collected_source.py"

# print(clean_jupyter_notebook(ipynb_input, clear_output=True, remove_empty_cells=True))
# , new_notebook_path=ipynb_output))

data_path_reso = {
    "datasource_path": "Cortex-data-library/cortex_data_library/docs/source/examples/data_end_to_end_examples/input",
    "datareference_path": "Cortex-data-library/cortex_data_library/docs/source/examples/data_end_to_end_examples/reference",
    "output_path": "Cortex-data-library/cortex_data_library/docs/source/examples/data_end_to_end_examples/output",
}

lines_to_comment = ["import project_path"]

extracted_lines = extract_code_from_jupyter_notebook(
    ipynb_input, data_path_reso, lines_to_comment, python_output
)


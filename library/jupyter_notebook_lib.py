import datetime
import time

MY_VERSION = "0.2"

def title_line_depth(source_line):
    if source_line[0:2] == "# ":
        return 1
    if source_line[0:3] == "## ":
        return 2
    if source_line[0:4] == "### ":
        return 3
    if source_line[0:5] == "#### ":
        return 4
    return -1



class JupyterCell:
    def __init__(self):
        self.cell_type = "undefined"
        self.id = ""
        self.source = []
        self.metadata = ""
        self.source_json = ""

    def _process_json_key(self, key, value):
        if key == "cell_type":
            self.cell_type = value
        elif key == "source":
            self.source = value
        elif key == "metadata":
            self.metadata = value
        else:
            print("unknown " + key)

        pass

    def _parse_json(self):
        for k,v in self.source_json.items():
            self._process_json_key(k,v)
        pass

    def load_from_json(self, json_str):
        self.source_json = json_str
        self._parse_json()

    def get_json_dict(self):
        dct = {}
        dct["cell_type"] = self.cell_type
        dct["metadata"] = self.metadata
        dct["source"] = self.source
        return dct

    def get_cell_source(self, code_cell_counter,
                        lines_to_comment,
                        data_path_resolution,
                        trace_execution
                        ):
        return []

    def is_empty(self):
        return len(self.source) == 0

    def get_cell_headers(self):
        return []

    def source_starts_with(self,search_str):
        if len(self.source) < 1:
            return False
        else:
            return self.source[0][0:len(search_str)] == search_str

    def get_table_of_content_elements(self):
        return []

class JupyterCellMarkdown(JupyterCell):
    def __init__(self):
        pass

    def get_table_of_content_elements(self):
        cell_source = self.source
        source_list = []

        for source_line in cell_source:
            source_line = source_line.replace("\n", "")
            source_line_depth = title_line_depth(source_line)
            if source_line_depth > 0:
                source_list.append(source_line)

        return source_list



class JupyterCellCode(JupyterCell):
    def __init__(self):
        super().__init__()
        self.output = []
        self.execution_count = ""

    def _process_json_key(self, key, value):
        if key == "outputs":
            self.output = value
        elif key == "execution_count":
            self.execution_count = value
        else:
            super()._process_json_key(key, value)
        pass

    def get_json_dict(self):
        dct = {}
        dct["cell_type"] = self.cell_type
        dct["execution_count"] = self.execution_count
        dct["metadata"] = self.metadata
        dct["outputs"] = self.output
        dct["source"] = self.source
        return dct

    def clear_output(self):
        self.output = []

    def get_cell_source(self, code_cell_counter,
                        lines_to_comment,
                        data_path_resolution,
                        trace_execution
                        ):
        cell_source = self.source
        has_import = False
        source_list = []

        for source_line in cell_source:
            source_line = source_line.replace("\n", "")

            has_import = has_import or source_line.strip()[0:7] == "import " or source_line.strip()[0:5] == "from "

            if source_line.strip() in lines_to_comment:
                source_line = "# " + source_line

            for k, v in data_path_resolution.items():
                if (
                        k == source_line.strip()[0: len(k)]
                        and source_line.find("=") > 1
                        and source_line.find(",") < 0
                ):
                    print(k, source_line)
                    pos_equal = source_line.find("=")
                    source_line = source_line[0: pos_equal + 1] + ' "' + v + '"'
                    print(k, source_line)

            source_list.append(source_line)

        if trace_execution and not has_import:
            source_list.append("")
            source_list.append(f"print(\"Done with cell {code_cell_counter}\")")
            source_list.append("")

        return source_list

class JupyterNotebook:
    def __init__(self):
        self.source_json = ""
        self.cells = []
        self.non_cells_tags = {}

    def load_from_json(self, json_str):
        self.source_json = json_str
        self._parse_json()

    def _parse_json(self):
        self.non_cells_tags = {}
        self.cells = []

        for k,v in self.source_json.items():
            if k != "cells":
                self.non_cells_tags[k] = v

        list_of_cells = self.source_json["cells"]
        for json_cell in list_of_cells:
            cell_type = json_cell["cell_type"]

            if cell_type == "code":
                cell = JupyterCellCode()

            elif cell_type == "markdown":
                cell = JupyterCellMarkdown()

            else:
                cell = JupyterCell()

            cell.load_from_json(json_cell)

            self.cells.append(cell)

        pass

    def get_json_dict(self):
        dct = {}
        cell_info = []
        for cell in self.cells:
            cell_info.append(cell.get_json_dict())

        dct["cells"] = cell_info
        for k, v in self.non_cells_tags.items():
            dct[k] = v

        return dct

    def remove_empty_cells(self):
        count_removed = 0
        temp_cells = []
        for cell in self.cells:
            if cell.is_empty():
                count_removed += 1
            else:
                temp_cells.append(cell)

        self.cells = temp_cells

    def clear_cells_output(self):
        for cell in self.cells:
            if isinstance(cell, JupyterCellCode):
                cell.clear_output()

    def get_notebook_source(self, lines_to_comment, data_path_resolution, trace_execution):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

        notebook_source = [
            "#",
            f"# Jupyter Notebook conversion utility version {MY_VERSION}",
            f"# Converted on {st}",
            "#",
        ]

        code_cell_counter = 0
        for cell in self.cells:
            if isinstance(cell, JupyterCellCode):
                code_cell_counter += 1
                cell_source = cell.get_cell_source(code_cell_counter,
                                                   lines_to_comment,
                                                   data_path_resolution,
                                                   trace_execution)

                notebook_source.append(f"# Cell {code_cell_counter}")

                for line in cell_source:
                    notebook_source.append(line)

        return notebook_source

    def get_notebook_table_of_content(self):
        current_toc_cell = None
        notebook_titles = []
        last_line_depth = -1

        for cell in self.cells:
            if cell.source_starts_with("## Content"):
                current_toc_cell = cell

            else:
                elements = cell.get_table_of_content_elements()
                for element in elements:
                    current_line_depth = title_line_depth(element)

                    if current_line_depth < last_line_depth and current_line_depth > 0:
                        notebook_titles.append("")

                    notebook_titles.append(element)

                    last_line_depth = current_line_depth

        return current_toc_cell, notebook_titles

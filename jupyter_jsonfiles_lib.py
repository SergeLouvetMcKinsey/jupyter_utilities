import json


def read_json_file(source_path):
    with open(source_path, "r") as file:
        notebook_source = file.readlines()

    return json.loads("\n".join(notebook_source))


def write_json_file(source_json, output_path):
    with open(output_path, "w") as file:
        file.writelines(json.dumps(source_json, indent=3))

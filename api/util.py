import importlib
import os
#print("Current Working Directory for util:", os.getcwd())
import os
import json


def save_json(data, file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_json(file_path):
    if not os.path.exists(file_path):
        raise ValueError(f"File {file_path} does not exist")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def import_class(class_path):
    #print("class_path is ", class_path)
    module_path, class_name = class_path.rsplit(".", 1)
    import os
    import sys
    #print("Current Working Directory:", os.getcwd())
    #print("module path is ", module_path)
    #print("class_name class is ", class_name)
    project_root = '/Users/ottavia/Downloads/GameBenchgioscofork'
    if project_root not in sys.path:
        sys.path.append(project_root)
    #try:
        #print("Current Working Directory try:", os.getcwd())
        #import sys
        #print("sys.path:", sys.path)
        #import agents
        #print("Import successful!")
   # except ModuleNotFoundError as e:
    #    print("Import failed with error:", e)
    module = importlib.import_module(module_path)
    #print("module is ", module)

    return getattr(module, class_name)
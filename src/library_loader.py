import yaml
import os
from deepmerge import always_merger
from library import Library

def load_library(library_filename):
    library_info = load_library_info(library_filename)
    root_path = os.path.dirname(library_filename)
    return Library(library_info, root_path)

def load_library_info(library_filename):
    library_info = open_file(library_filename)
    root_path = os.path.dirname(library_filename)
    for filename in library_info.get('Files', []):
        filepath = os.path.join(root_path, filename)
        loaded_info = load_library_info(filepath)
        library_info = always_merger.merge(library_info, loaded_info)
    return library_info


def open_file(filename):
    with open(filename) as file:
        data = yaml.safe_load(file)
    return data
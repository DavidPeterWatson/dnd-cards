import yaml
import os
from deepmerge import always_merger
from cdb.library import Library

def load_library(library_filename, library_info = {}):
    library_info = merge_library_info(load_library_info(library_filename), library_info)
    root_path = os.path.dirname(library_filename)
    return Library(library_info, root_path)

def load_library_info(library_filename):
    library_info = open_file(library_filename)
    root_path = os.path.dirname(library_filename)
    path = library_info.get('Path', '')
    for filename in library_info.get('Files', []):
        filepath = os.path.join(root_path, path, filename)
        loaded_info = load_library_info(filepath)
        library_info = merge_library_info(library_info, loaded_info)
    return library_info

def merge_library_info(library_info, loaded_info):
    return always_merger.merge(library_info, loaded_info)

def open_file(filename):
    with open(filename) as file:
        data = yaml.safe_load(file)
    return data
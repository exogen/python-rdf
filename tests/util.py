import os.path


def get_data_path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)

def open_data_file(filename, mode='r'):
    return open(get_data_path(filename), mode)


import os
import shutil


def extend_dict(d1: dict, d2: dict):
    """Extend d1 by d2 content"""

    return {**d1, **d2}


def log(msg):
    print(f'[LOG] {msg}')


def warn(msg):
    print(f'[WARN] {msg}')


def file_exists(path: str):
    return os.path.exists(path)


def remove_file_if_exists(path: str):
    if os.path.exists(path):
        print()
        warn(f'File {path} exists, removing...')


def empty_directory_if_exists_then_create(path: str):
    if os.path.isdir(path):
        print()
        warn(f'Directory {path} exists, removing...')

        shutil.rmtree(path)

    log(f'Creating directory {path}...')
    os.mkdir(path)

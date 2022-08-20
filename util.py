from datetime import datetime, timezone
from os import mkdir
from os.path import exists as path_exists, isdir as path_isdir
from random import choice as random_choice
from shutil import rmtree
from string import ascii_lowercase
from time import strftime


def extend_dict(d1: dict, d2: dict) -> dict:
    """Extend d1 by d2 content"""

    return {**d1, **d2}


def log(msg: str) -> None:
    print(f'[LOG] {msg}')


def info(msg: str) -> None:
    print(f'[INFO] {msg}')


def warn(msg) -> None:
    print(f'[WARN] {msg}')


def file_exists(path: str) -> bool:
    return path_exists(path)


def remove_file_if_exists(path: str) -> None:
    if path_exists(path):
        print()
        warn(f'File {path} exists, removing...')


def get_random_user_agent() -> str:
    """
    Return a random string which can be used as user agent, as reusing one can throw errors
    @return: user agent
    """

    letters = ascii_lowercase
    return ''.join(random_choice(letters) for i in range(len(letters)))


def empty_directory_if_exists_then_create(path: str) -> None:
    if path_isdir(path):
        print()
        warn(f'Directory {path} exists, removing...')

        rmtree(path)

    log(f'Creating directory {path}...')
    mkdir(path)


def get_current_timestamp_utc() -> float:
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)

    return utc_time.timestamp()


def get_current_day_month_year() -> str:
    return strftime("%d.%m.%Y")


if __name__ == '__main__':
    """testing"""
    print(get_current_day_month_year())

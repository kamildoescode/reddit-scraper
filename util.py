def extend_dict(d1: dict, d2: dict):
    """Extend d1 by d2 content"""

    return {**d1, **d2}


def log(msg):
    print(f'[LOG] {msg}')

from typing import List


def is_positive_int(n):
    return n.isdigit()


def convert_to_bool(bool_string: str):
    """
    Careful: True or False is valid. Check if is None to see if this conversion failed
    """
    if bool_string.lower() in ['false', 'no', 'off', 'disable']:
        return False
    elif bool_string.lower() in ['true', 'yes', 'on', 'enable']:
        return True
    return None


def int_to_place(n: int) -> str:
    """
    Convert a number to a place.
    """
    last_digit = int(repr(n)[-1])
    last_two_digits = int(repr(n)[-2:])
    suffix = 'th'
    if last_digit == 1 and last_two_digits != 11:
        suffix = 'st'
    elif last_digit == 2 and last_two_digits != 12:
        suffix = 'nd'
    elif last_digit == 3 and last_two_digits != 13:
        suffix = 'rd'
    return f"{n}{suffix}"


class DynamicClassCreator:
    def __init__(self):
        self.created_classes = {}

    def __call__(self, bases: List):
        rep = ",".join([i.__name__ for i in bases])
        if rep in self.created_classes:
            return self.created_classes[rep]

        class DynamicClass(*bases):
            pass

        self.created_classes[rep] = DynamicClass
        return DynamicClass

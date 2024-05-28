import re


def mask_password(value: str):
    """remove the password from this postgresql connect string so we don't write it to logs, etc.

    Args:
        value (str): the unmasked string containing one or more postgres connect string.

    Returns:
        _type_: the string with the password replaced by MASKED
    """
    return re.sub(":\w+@", ":MASKED@", value)

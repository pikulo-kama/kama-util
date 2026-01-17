
def is_float(string: str):
    """
    Checks if a string represents a valid floating-point number.

    Args:
        string (str): The string to evaluate.

    Returns:
        bool: True if the string can be cast to a float, False otherwise.
    """

    if "." not in string:
        return False

    try:
        value = float(string)
        return value is not None

    except ValueError:
        return False

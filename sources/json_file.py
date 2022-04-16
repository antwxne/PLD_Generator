#!/bin/env python3
from json import load
from os import path


def get_json_from_file(filename: str) -> dict:
    """ Parse a file containing a json

    Args:
        filename (String): name of the file to parse

    Raises:
        ValueError: file doesn't exist or is not a file

    Returns:
        Any: json parsed
    """
    if path.exists(filename) and path.isfile(filename):
        file = open(filename, "r")
        json_data = load(file)
        file.close()
        return json_data
    else:
        raise ValueError("Wrong filename: " + filename + " doesn't exist")
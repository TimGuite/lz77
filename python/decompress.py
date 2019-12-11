"""Complement to the compress.py file, this will decompress files from their compressed state"""

from typing import List, Tuple


def decompress(compressed: List[Tuple[int, int, str]]) -> str:
    """Turn the list of (offset, length, char) into an output string"""

    output = ""

    for value in compressed:
        offset = value[0]
        length = value[1]
        char = value[2]

        if length == 0:
            if char is not None:
                output += char
        else:
            start_index = len(output) - offset
            for i in range(length):
                output += output[start_index + i]

    return output

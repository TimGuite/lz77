"""Complement to the compress.py file, this will decompress files from their compressed state"""

from typing import List, Tuple


def decompress(compressed: List[Tuple[int, int, str]]) -> str:
    """Turn the list of (offset, length, char) into an output string"""

    output = ""

    for value in compressed:
        offset, length, char = value

        if length == 0:
            if char is not None:
                output += char
        else:
            start_index = len(output) - offset
            for i in range(length):
                output += output[start_index + i]

    return output

def from_bytes(compressed_bytes: bytes) -> [(int, int, str)]:
    """Take in the compressed format and return a higher level representation"""
    # Currently using 5 bits for offset and 3 bits for length
    assert len(compressed_bytes) % 2 == 0

    output = []

    for index in range(len(compressed_bytes) // 2):
        counts = compressed_bytes[2*index]
        char = compressed_bytes[(2*index)+1]

        offset = (counts & 0b11111000) >> 3
        length = counts & 0b00000111

        if char == b'\x00':
            char_out = None
        else:
            char_out = chr(char)
        output.append((offset, length, char_out))

    return output
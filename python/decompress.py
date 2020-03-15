"""Complement to the compress.py file, this will decompress files from their compressed state"""

import logging
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
            if offset == 0:
                if char is not None:
                    output += char
                    length -= 1
                    offset = 1
            start_index = len(output) - offset
            for i in range(length):
                output += output[start_index + i]

    return output


def from_bytes(
    compressed_bytes: bytearray, offset_bits: int = 11, length_bits: int = 5,
) -> [(int, int, str)]:
    """Take in the compressed format and return a higher level representation"""

    assert (
        offset_bits + length_bits
    ) % 8 == 0, f"Please provide offset_bits and length_bits which add up to a multiple of 8, so they can be efficiently packed. Received {offset_bits} and {length_bits}."
    offset_length_bytes = int((offset_bits + length_bits) / 8)

    output = []

    while len(compressed_bytes) > 0:
        offset_length_value = 0
        for _ in range(offset_length_bytes):
            offset_length_value = (offset_length_value * 256) + int(
                compressed_bytes.pop(0)
            )

        offset = offset_length_value >> length_bits
        length = offset_length_value & ((2 ** length_bits) - 1)
        logging.debug(f"Offset: {offset}")
        logging.debug(f"Length: {length}")

        if offset > 0:
            char_out = None
        else:
            # Get the next character and convert to an ascii character
            char_out = str(chr(compressed_bytes.pop(0)))

        output.append((offset, length, char_out))

    return output


def decompress_file(input_file: str, output_file: str):
    """Open and read an input file, decompress it, and write the compressed
    values to the output file"""
    try:
        with open(input_file, "rb") as f:
            input_array = bytearray(f.read())
    except FileNotFoundError:
        print(f"Could not find input file at: {input_file}")
        raise
    except Exception:
        raise

    compressed_input = decompress(from_bytes(input_array))

    with open(output_file, "w") as f:
        f.write(compressed_input)

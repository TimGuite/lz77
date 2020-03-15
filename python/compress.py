import logging


def compress(
    input_string: str, max_offset: int = 2047, max_length: int = 31
) -> [(int, int, str)]:
    """Compress the input string into a list of length, offset, char values"""

    # Create the input
    input_array = str(input_string[:])

    # Create a string of the characters which have been passed
    window = ""

    ## Store output in this list
    output = []

    while input_array != "":
        length, offset = best_length_offset(window, input_array, max_length, max_offset)
        output.append((offset, length, input_array[0]))
        window += input_array[:length]
        input_array = input_array[length:]

    return output


def to_bytes(
    compressed_representation: [(int, int, str)],
    offset_bits: int = 11,
    length_bits: int = 5,
) -> bytearray:
    """Turn the compression representation into a byte array"""
    output = bytearray()

    assert (
        offset_bits + length_bits
    ) % 8 == 0, f"Please provide offset_bits and length_bits which add up to a multiple of 8, so they can be efficiently packed. Received {offset_bits} and {length_bits}."
    offset_length_bytes = int((offset_bits + length_bits) / 8)

    for value in compressed_representation:
        offset, length, char = value
        assert (
            offset < 2 ** offset_bits
        ), f"Offset of {offset} is too large, only have {offset_bits} to store this value"
        assert (
            length < 2 ** length
        ), f"Length of {length} is too large, only have {length} to store this value"

        offset_length_value = (offset << length_bits) + length
        logging.debug(f"Offset: {offset}")
        logging.debug(f"Length: {length}")
        logging.debug(f"Offset and length: 0b{offset_length_value:b}")

        for count in range(offset_length_bytes):
            output.append(
                (offset_length_value >> (8 * (offset_length_bytes - count - 1)))
                & (0b11111111)
            )

        if char is not None:
            if offset == 0:
                output.append(ord(char))
        else:
            output.append(0)

    return output


def best_length_offset(
    window: str, input_string: str, max_length: int = 15, max_offset: int = 4095
) -> (int, int):
    """Take the window and an input string and return the offset and length
    with the biggest length of the input string as a substring"""

    if max_offset < len(window):
        cut_window = window[-max_offset:]
    else:
        cut_window = window

    # Return (0, 0) if the string provided is empty
    if input_string is None or input_string == "":
        return (0, 0)

    # Initialise result parameters - best case so far
    length, offset = (1, 0)

    # This should also catch the empty window case
    if input_string[0] not in cut_window:
        best_length = repeating_length_from_start(input_string[0], input_string[1:])
        return (min((length + best_length), max_length), offset)

    # Best length now zero to allow occurences to take priority
    length = 0

    # Test for every string in the window, in reverse order to keep the offset as low as possible
    # Look for either the whole window or up to max offset away, whichever is smaller
    for index in range(1, (len(cut_window) + 1)):
        # Get the character at this offset
        char = cut_window[-index]
        if char == input_string[0]:
            found_offset = index
            # Collect any further strings which can be found
            found_length = repeating_length_from_start(
                cut_window[-index:], input_string
            )
            if found_length > length:
                length = found_length
                offset = found_offset

    # Only return up to the maximum length
    # This will capture the maximum number of characters allowed
    # although it might not capture the maximum amount of characters *possible*
    return (min(length, max_length), offset)


def repeating_length_from_start(window: str, input_string: str) -> int:
    """Get the maximum repeating length of the input from the start of the window"""
    if window == "" or input_string == "":
        return 0

    if window[0] == input_string[0]:
        return 1 + repeating_length_from_start(
            window[1:] + input_string[0], input_string[1:]
        )
    else:
        return 0


def compress_file(input_file: str, output_file: str):
    """Open and read an input file, compress it, and write the compressed
    values to the output file"""
    try:
        with open(input_file) as f:
            input_array = f.read()
    except FileNotFoundError:
        print(f"Could not find input file at: {input_file}")
        raise
    except Exception:
        raise

    compressed_input = to_bytes(compress(input_array))

    with open(output_file, "wb") as f:
        f.write(compressed_input)

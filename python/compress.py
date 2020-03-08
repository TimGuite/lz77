def compress(input_string: str) -> [(int, int, str)]:
    """Compress the input string into a list of length, offset, char values"""

    # Create the input
    input_array = input_string[:]

    # Create a string of the characters which have been passed
    window = ""

    ## Store output in this list
    output = []

    while input_array is not "":
        # print(f"Input: {input_array}")
        # print(f"Window: {window}")
        # Number of characters to go back
        offset = 0
        # Number of characters to go forwards from this point
        length = 0

        matched_term = input_array[0]

        while input_array[: (length + 1)] in window and (length + 1) <= len(
            input_array
        ):
            length += 1

        if length == 0:
            matched_term = input_array[0]
        else:
            matched_term = input_array[:length]
        # print(f"Matched: {matched_term}")

        if length > 0:
            offset = len(window) - window.find(matched_term)

        if length == 0 or length < len(input_array):
            next_character = input_array[length]
        else:
            next_character = None

        result = (offset, length, next_character)

        output.append(result)

        if length == 0:
            input_array = input_array[1:]
        else:
            input_array = input_array[length:]
        window += matched_term

    return output


def to_bytes(compressed_representation: [(int, int, str)]) -> bytes:
    """Turn the compression representation into a byte array"""
    output = bytes()

    for value in compressed_representation:
        """5 bits for offset, 3 for length, 1 byte for character"""
        offset, length, char = value
        if char is not None:
            output = (
                output
                + ((offset << 3) + length).to_bytes(1, byteorder="big")
                + char.encode("utf-8")
            )
        else:
            output = (
                output + ((offset << 3) + length).to_bytes(1, byteorder="big") + b"\x00"
            )

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
        best_length, _ = best_length_offset(input_string[0], input_string[1:])
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


a = best_length_offset("", "a")
b = best_length_offset("a123", "a")
c = best_length_offset("", "aaaaa")
d = best_length_offset("abc ab a", "abc")
e = best_length_offset("", "aaaaa", max_length=3)
print("Done")

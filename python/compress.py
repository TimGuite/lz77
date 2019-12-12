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
            output = output + ((offset << 3) + length).to_bytes(1, byteorder='big') + char.encode('utf-8')
        else:
            output = output + ((offset << 3) + length).to_bytes(1, byteorder='big') + b'\x00'

    return output
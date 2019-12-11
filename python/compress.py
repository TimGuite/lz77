def compress(input_string: str) -> [(int, int, str)]:
    """Compress the input string into a list of length, offset, char values"""

    # Create the input
    input_array = input_string[:]

    # Create a string of the characters which have been passed
    window = ""

    ## Store output in this list
    output = []

    while input_array is not "":
        print(input_array)
        # Number of characters to go back
        offset = 0
        # Number of characters to go forwards from this point
        length = 0

        while input_array[: (length + 1)] in window and (length + 1) <= len(
            input_array
        ):
            length += 1

        matched_term = input_array[: (length + 1)]

        if length > 0:
            offset = len(window) - window.find(matched_term)

        if length == 0 or length < len(input_array):
            next_character = input_array[length]
        else:
            next_character = None

        result = [offset, length, next_character]

        output.append(result)

        input_array = input_array[(length + 1) :]
        window += matched_term

    return output


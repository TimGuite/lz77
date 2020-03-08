from compress import best_length_offset


def test_provides_useable_response_for_no_input():
    assert best_length_offset("", "") == (0, 0)


def test_gets_letter_from_front_of_window():
    assert best_length_offset("abcdefg", "a") == (1, 7)


def test_zero_offset_when_window_is_empty():
    assert best_length_offset("", "a") == (1, 0)


def test_gets_repeated_values_when_not_in_window():
    assert best_length_offset("", "aaaaaa") == (6, 0)


def test_gets_repeated_value_when_value_in_window():
    assert best_length_offset("a", "aaaaaa") == (6, 1)


def test_gets_repeating_pattern_from_window():
    assert best_length_offset("ab", "ababab") == (6, 2)


def test_gets_longest_occurrence_in_window():
    assert best_length_offset("abc ab a", "abc") == (3, 8)


def test_returns_only_up_to_maximum_length():
    assert best_length_offset("", "aaaaa", max_length=3) == (3, 0)


def test_looks_only_up_to_max_offset():
    assert best_length_offset("a12345", "a", max_offset=3) == (1, 0)

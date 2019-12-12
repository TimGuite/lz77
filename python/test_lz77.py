"""Unit tests for compression and decompression"""

import string
from hypothesis import given, example
from hypothesis.strategies import text, characters

from compress import compress, to_bytes
from decompress import decompress, from_bytes


def test_it_compresses_a_simple_example():
    assert decompress(compress("This is a simple test")) == "This is a simple test"


"""Property based testing with hypothesis"""


@given(text())
def test_decompress_inverts_compress(s):
    assert decompress(compress(s)) == s


class Test_To_And_From_Bytes_For_Simple_Strings():
    def test_one_character(self):
        assert decompress(from_bytes(to_bytes(compress("a")))) == "a"

        
    def test_multiple_character(self):
        assert decompress(from_bytes(to_bytes(compress("abcdefg")))) == "abcdefg"

        
    def test_repeated_characters(self):
        assert decompress(from_bytes(to_bytes(compress("aaaaa")))) == "aaaaa"

    # Only ascii at the moment
    @given(characters(max_codepoint=8, whitelist_characters=string.printable))
    def test_simple_strings(self, s):
        assert decompress(from_bytes(to_bytes(compress(s)))) == s
"""Unit tests for compression and decompression"""

from hypothesis import given, example
from hypothesis.strategies import text

from compress import compress
from decompress import decompress


def test_it_compresses_a_simple_example():
    assert decompress(compress("This is a simple test")) == "This is a simple test"


"""Property based testing with hypothesis"""


@given(text())
def test_decompress_inverts_compress(s):
    assert decompress(compress(s)) == s

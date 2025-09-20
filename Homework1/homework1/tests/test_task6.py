import pytest
from homework1.src.task6 import count_words

@pytest.mark.parametrize("filename, expected_count", [
    ("task6_read_me.txt", 127),
    ("nonexistent.txt", -1),  # Expect -1 for missing file
])
def test_word_count(filename, expected_count):
    assert count_words(filename) == expected_count

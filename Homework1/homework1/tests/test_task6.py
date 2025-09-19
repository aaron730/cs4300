import pytest
from homework1.src.task6 import count_words

def test_word_count():
    assert count_words("task6_read_me.txt") == 127
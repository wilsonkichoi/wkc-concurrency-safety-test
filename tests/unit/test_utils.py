import pytest
from wkc_concurrency_safety_test.utils import inflate_and_shuffle


def test_inflate_and_shuffle_size_greater_than_data_length():
    data = [1, 2, 3, 4, 5]
    size = 20
    result = inflate_and_shuffle(data, size)
    assert len(result) == size

def test_inflate_and_shuffle_size_less_than_data_length():
    data = [1, 2, 3, 4, 5]
    size = 3
    result = inflate_and_shuffle(data, size)
    assert len(result) == size

def test_inflate_and_shuffle_size_equal_to_data_length():
    data = [1, 2, 3, 4, 5]
    size = 5
    result = inflate_and_shuffle(data, size)
    assert len(result) == size
import pytest

from anyocr.client import _process_page_range


def test_page_set():
    r = _process_page_range("0,1")
    assert r == [0, 1]

def test_page_range():
    r = _process_page_range("4-6")
    assert r == [4, 5, 6]

def test_page_range_multi():
    r = _process_page_range("1,4-8,12")
    assert r == [1, 4, 5, 6, 7, 8, 12]

def test_incorrect_range_fails():
    with pytest.raises(ValueError):
        _process_page_range("2-1")

def test_misformatted_range_fails():
    with pytest.raises(ValueError):
        _process_page_range("--1")

    with pytest.raises(ValueError):
        _process_page_range("-1")

    with pytest.raises(ValueError):
        _process_page_range("-1")

    with pytest.raises(ValueError):
        _process_page_range("1,")

import pytest
from validation import (
    ask_user_number,
    check_positive_assert,
    count_vowels,
    create_name,
)


@pytest.mark.parametrize("number", [1, 0.5, 100])
def test_check_positive_assert_ok(number):
    assert check_positive_assert(number) == number


@pytest.mark.parametrize("number", [0, -1, -0.1])
def test_check_positive_assert_fails(number):
    with pytest.raises(AssertionError):
        check_positive_assert(number)


def test_create_name_ok():
    assert create_name("Оля") == "Оля"


def test_create_name_empty():
    with pytest.raises(ValueError):
        create_name("")


@pytest.mark.parametrize("text, expected", [
    ("", 0),
    ("Hello", 2),
    ("Привіт", 2),
    ("AEIOU", 5),
    ("bcdfg", 0),
])
def test_count_vowels(text, expected):
    assert count_vowels(text) == expected


def test_ask_user_number(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _prompt: "42")
    assert ask_user_number() == "42"

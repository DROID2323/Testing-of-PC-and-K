"""Тест БЕЗ assert: викликає код і дає високе покриття, але нічого не перевіряє."""
from unittest.mock import patch

from app import Figure, main
from validation import ask_user_number, check_positive_assert, count_vowels, create_name


def test_weak_calls_everything():
    for kind in ("квадрат", "прямокутник", "трикутник"):
        f = Figure(kind, 5)
        f.get_angles
        f.get_figure_type
        f.get_figure_length
        str(f)
    try:
        Figure("коло", 5)
    except ValueError:
        pass
    try:
        Figure("квадрат", 0)
    except ValueError:
        pass
    main()
    check_positive_assert(1)
    try:
        check_positive_assert(0)
    except AssertionError:
        pass
    create_name("Оля")
    try:
        create_name("")
    except ValueError:
        pass
    count_vowels("Привіт")
    with patch("builtins.input", return_value="1"):
        ask_user_number()

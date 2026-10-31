import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from app import Figure, main
from validation import (
    ask_user_number,
    check_positive_assert,
    count_vowels,
    create_name,
)


class FigureTests(unittest.TestCase):
    def test_angles(self):
        for kind, expected in (("квадрат", 4), ("прямокутник", 4), ("трикутник", 3)):
            with self.subTest(kind=kind):
                self.assertEqual(Figure(kind, 5).get_angles, expected)

    def test_properties_and_str(self):
        f = Figure("квадрат", 10)
        self.assertEqual(f.get_figure_type, "квадрат")
        self.assertEqual(f.get_figure_length, 10)
        self.assertIn("квадрат", str(f))

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            Figure("коло", 5)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", 0)

    def test_main(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            main()
        self.assertIn("трикутник", buf.getvalue())


class ValidationTests(unittest.TestCase):
    def test_check_positive(self):
        self.assertEqual(check_positive_assert(3), 3)
        with self.assertRaises(AssertionError):
            check_positive_assert(0)

    def test_create_name(self):
        self.assertEqual(create_name("Оля"), "Оля")
        with self.assertRaises(ValueError):
            create_name("")

    def test_count_vowels(self):
        self.assertEqual(count_vowels("Привіт"), 2)
        self.assertEqual(count_vowels(""), 0)

    def test_ask_user_number(self):
        with patch("builtins.input", return_value="7"):
            self.assertEqual(ask_user_number(), "7")


if __name__ == "__main__":
    unittest.main()

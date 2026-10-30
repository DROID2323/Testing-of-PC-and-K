import unittest
from unittest.mock import patch

from app import Figure
from validation import check_positive_assert, count_vowels, create_name, ask_user_number


class TestValidation(unittest.TestCase):

    def test_assert_positive_number_ok(self):
        self.assertEqual(5, check_positive_assert(5))

    def test_assert_negative_raises(self):
        with self.assertRaises(AssertionError):
            check_positive_assert(-1)

    def test_assert_zero_raises(self):
        with self.assertRaises(AssertionError):
            check_positive_assert(0)

    def test_create_name_ok(self):
        self.assertEqual("Іван", create_name("Іван"))

    def test_create_name_empty_raises(self):
        with self.assertRaises(ValueError):
            create_name("")


class TestCountVowels(unittest.TestCase):

    def test_english_vowels(self):
        self.assertEqual(2, count_vowels("apple"))

    def test_no_vowels(self):
        self.assertEqual(0, count_vowels("gym"))

    def test_all_vowels(self):
        self.assertEqual(3, count_vowels("aei"))

    def test_empty_string(self):
        self.assertEqual(0, count_vowels(""))

    def test_digits_only(self):
        self.assertEqual(0, count_vowels("12345"))

    def test_ukrainian_letters(self):
        self.assertEqual(2, count_vowels("привіт"))
        self.assertEqual(4, count_vowels("україна"))


class TestFigureType(unittest.TestCase):

    def test_square_type(self):
        f = Figure("квадрат", 5)
        self.assertEqual("квадрат", f.get_figure_type)

    def test_rectangle_type(self):
        f = Figure("прямокутник", 3)
        self.assertEqual("прямокутник", f.get_figure_type)

    def test_triangle_type(self):
        f = Figure("трикутник", 7)
        self.assertEqual("трикутник", f.get_figure_type)


class TestFigureLength(unittest.TestCase):

    def setUp(self):
        self.square = Figure("квадрат", 10)

    def tearDown(self):
        del self.square

    def test_length_is_correct(self):
        self.assertEqual(10, self.square.get_figure_length)

    def test_zero_length_raises(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", 0)

    def test_negative_length_raises(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", -5)

    def test_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            Figure("коло", 5)


class TestFigureAngles(unittest.TestCase):

    def test_square_angles(self):
        self.assertEqual(4, Figure("квадрат", 5).get_angles)

    def test_rectangle_angles(self):
        self.assertEqual(4, Figure("прямокутник", 5).get_angles)

    def test_triangle_angles(self):
        self.assertEqual(3, Figure("трикутник", 5).get_angles)


class TestFigureSubTest(unittest.TestCase):

    def test_figure_lengths_subtest(self):
        for length in [1, 5, 10]:
            with self.subTest(length=length):
                f = Figure("квадрат", length)
                self.assertEqual(length, f.get_figure_length)

    def test_all_figure_types_subtest(self):
        for figure_type in ["квадрат", "прямокутник", "трикутник"]:
            with self.subTest(figure_type=figure_type):
                f = Figure(figure_type, 4)
                self.assertEqual(figure_type, f.get_figure_type)


class TestMockInput(unittest.TestCase):

    @patch("builtins.input", return_value="5")
    def test_ask_user_number_returns_value(self, mock_input):
        result = ask_user_number()
        self.assertEqual("5", result)
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="")
    def test_ask_user_number_empty(self, mock_input):
        result = ask_user_number()
        self.assertEqual("", result)


if __name__ == "__main__":
    unittest.main()
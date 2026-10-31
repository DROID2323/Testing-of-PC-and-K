"""Еквівалент pytest-тестів на unittest — для порівняння двох підходів."""
import unittest

from app import Figure


class TestFigure(unittest.TestCase):
    def test_figure_type(self):
        figure = Figure("трикутник", 4)
        self.assertEqual(figure.get_figure_type, "трикутник")

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", 0)


if __name__ == "__main__":
    unittest.main()

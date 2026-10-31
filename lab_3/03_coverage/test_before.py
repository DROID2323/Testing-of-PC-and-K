"""Початковий стан із лабораторної: протестовано лише трикутник."""
from app import Figure


def test_triangle_only():
    assert Figure("трикутник", 3).get_angles == 3

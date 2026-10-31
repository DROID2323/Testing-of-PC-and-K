import pytest
from app import Figure


# ──────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────

@pytest.fixture
def square():
    """Fixture з довжиною 10 — використовується у кількох тестах."""
    return Figure("квадрат", 10)


@pytest.fixture(scope="module")
def allowed_figures():
    """Module-scope fixture — повертає список дозволених фігур."""
    return Figure.VALID_TYPES


# ──────────────────────────────────────────────────────────────
# Базові тести типу та довжини
# ──────────────────────────────────────────────────────────────

@pytest.mark.unit
def test_figure_type():
    """Перевіряє, що тип фігури зберігається правильно."""
    figure = Figure("трикутник", 4)
    assert figure.get_figure_type == "трикутник"


@pytest.mark.unit
def test_figure_length():
    """Перевіряє, що довжина сторони зберігається правильно."""
    figure = Figure("прямокутник", 7.5)
    assert figure.get_figure_length == 7.5


def test_square_length_via_fixture(square):
    """Перевіряє довжину через fixture зі значенням 10."""
    assert square.get_figure_length == 10


def test_square_type_via_fixture(square):
    """Перевіряє тип через ту саму fixture."""
    assert square.get_figure_type == "квадрат"


def test_square_angles_via_fixture(square):
    """Перевіряє кількість кутів квадрата через fixture."""
    assert square.get_angles == 4


# ──────────────────────────────────────────────────────────────
# Параметризований тест: всі дозволені фігури
# ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("figure_type", Figure.VALID_TYPES)
def test_allowed_figure(figure_type):
    """Перевіряє, що кожен дозволений тип успішно створюється."""
    figure = Figure(figure_type, 1)
    assert figure.get_figure_type == figure_type


# ──────────────────────────────────────────────────────────────
# Тести кутів для кожного типу фігури
# ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("figure_type, expected_angles", [
    ("квадрат", 4),
    ("прямокутник", 4),
    ("трикутник", 3),
])
def test_angles(figure_type, expected_angles):
    """Перевіряє кількість кутів для кожної фігури."""
    figure = Figure(figure_type, 5)
    assert figure.get_angles == expected_angles


# ──────────────────────────────────────────────────────────────
# Тести на неправильні типи фігур
# ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("invalid_type", [
    "коло",
    "ромб",
    "трапеція",
    "",
    "КВАДРАТ",
    "triangle",
    123,
])
def test_invalid_figure_type(invalid_type):
    """Кожен невідомий тип має викидати ValueError."""
    with pytest.raises((ValueError, TypeError)):
        Figure(invalid_type, 5)


# ──────────────────────────────────────────────────────────────
# Тести на неправильні значення довжини
# ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("invalid_length", [
    0,
    -1,
    -100,
    -0.001,
])
def test_invalid_length(invalid_length):
    """Довжина ≤ 0 має викидати ValueError."""
    with pytest.raises(ValueError):
        Figure("квадрат", invalid_length)


# ──────────────────────────────────────────────────────────────
# Перевірка рядкового представлення
# ──────────────────────────────────────────────────────────────

def test_str_representation():
    """Перевіряє __str__ фігури."""
    figure = Figure("трикутник", 3)
    assert "трикутник" in str(figure)
    assert "3" in str(figure)


# ──────────────────────────────────────────────────────────────
# Тести з module-scope fixture
# ──────────────────────────────────────────────────────────────

def test_all_valid_types_in_allowed_figures(allowed_figures):
    """Module-scope fixture повертає всі типи, і їх рівно 3."""
    assert len(allowed_figures) == 3


def test_triangle_in_allowed_figures(allowed_figures):
    """Module-scope fixture: трикутник присутній у списку типів."""
    assert "трикутник" in allowed_figures

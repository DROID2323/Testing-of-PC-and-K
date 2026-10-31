# Лабораторна робота — Тестування з бібліотекою pytest

## Структура проєкту

```
lab_2/
├── pyproject.toml
├── README.md
└── 02_pytest/
    ├── app.py          # клас Figure
    ├── validation.py   # допоміжні функції
    └── test_app.py     # pytest-тести
```

---

## Встановлення pytest

```bash
pip install pytest
# або через poetry
poetry add --group dev pytest
```

---

## Запуск тестів

```bash
# всі тести з детальним виводом
pytest 02_pytest/test_app.py -v

# тільки unit-тести
pytest 02_pytest/test_app.py -m unit -v

# показати всі знайдені тести без запуску
pytest --collect-only

# зупинитись після першої помилки
pytest -x --tb=short
```

---

## Результат запуску `pytest -v`


![alt text](/lab_2/02_pytest/1.png)



## Різниця між `unittest.TestCase` та функцією `pytest`

| Критерій | `unittest.TestCase` | pytest-функція |
|---|---|---|
| Структура | Клас, що успадковує `TestCase` | Звичайна функція з префіксом `test_` |
| Перевірки | `self.assertEqual(a, b)`, `self.assertRaises(...)` | Звичайний `assert a == b`, `pytest.raises(...)` |
| Запуск | `python -m unittest` | `pytest` |
| Fixtures | `setUp` / `tearDown` методи класу | Декоратор `@pytest.fixture`, будь-яка область видимості |
| Параметризація | Потребує сторонніх бібліотек або ручного циклу | Вбудований `@pytest.mark.parametrize` |
| Повідомлення | Стандартне, менш детальне | Детальний diff при провалі |

**Приклад unittest:**
```python
import unittest
from app import Figure

class TestFigure(unittest.TestCase):
    def test_figure_type(self):
        figure = Figure("трикутник", 4)
        self.assertEqual(figure.get_figure_type, "трикутник")

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", 0)
```

**Еквівалент у pytest:**
```python
from app import Figure

def test_figure_type():
    figure = Figure("трикутник", 4)
    assert figure.get_figure_type == "трикутник"

def test_invalid_length():
    with pytest.raises(ValueError):
        Figure("квадрат", 0)
```

---

## Приклади використання параметризації, fixture та маркера

### Параметризація
Один тест запускається для кожного елемента списку автоматично:
```python
@pytest.mark.parametrize("figure_type", ["квадрат", "прямокутник", "трикутник"])
def test_allowed_figure(figure_type):
    assert Figure(figure_type, 1).get_figure_type == figure_type
```

### Fixture
Підготовлює спільний об'єкт для кількох тестів:
```python
@pytest.fixture
def square():
    return Figure("квадрат", 10)

def test_square_length(square):
    assert square.get_figure_length == 10
```

### Fixture зі scope="module"
Об'єкт створюється один раз для всього модуля:
```python
@pytest.fixture(scope="module")
def allowed_figures():
    return Figure.VALID_TYPES

def test_count(allowed_figures):
    assert len(allowed_figures) == 3

def test_triangle_present(allowed_figures):
    assert "трикутник" in allowed_figures
```

### Маркер
Дозволяє запускати лише вибрані тести:
```python
@pytest.mark.unit
def test_figure_type():
    assert Figure("трикутник", 4).get_figure_type == "трикутник"
```
```bash
pytest -m unit -v   # запустить тільки тести з маркером unit
```

---

## Навмисно зламаний тест та `pytest -x --tb=short`

Якщо змінити очікуване значення у `test_figure_type`:
```python
def test_figure_type():
    figure = Figure("трикутник", 4)
    assert figure.get_figure_type == "квадрат"  # навмисна помилка
```

Результат `pytest -x --tb=short`:
```
FAILED 02_pytest/test_app.py::test_figure_type - AssertionError: assert 'трикутник' == 'квадрат'
```
Прапор `-x` зупиняє виконання після першої помилки, `--tb=short` показує лише коротке повідомлення без повного traceback — зручно для швидкого пошуку проблеми.

### Висновок:

### Висновок:

- В роботі реалізовано юніт-тестування на Python за допомогою бібліотеки `pytest`
- Мету роботи досягнуто — написано 25 тестів для класу `Figure`
- Отримано знання про `pytest.fixture`, `pytest.mark.parametrize`, `pytest.raises` та маркери
- Вивчено різницю між `unittest.TestCase` і pytest-функціями — pytest простіший і лаконічніший
- Всі 25 тестів пройшли успішно (`25 passed in 0.06s`)
- Складність виникла з налаштуванням середовища — `pytest` не розпізнавався без `python -m pytest`
- Формат здачі через GitHub зручний і наочний

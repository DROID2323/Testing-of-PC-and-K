# Звіт до роботи
## Тема: Загальне тестування та юніт-тести
### Мета роботи: Навчитися писати юніт-тести на Python за допомогою бібліотеки unittest, використовувати assert, raise ValueError, setUp/tearDown, subTest та mock.

---
### Виконання роботи

* **Завдання 1 — Перевірка даних**
    1. Створили функцію `check_positive_assert` з перевіркою через `assert`
    2. Створили функцію `create_name` з перевіркою через `raise ValueError`
    3. Перевірили обидві функції — для правильного введення функції повертають значення, для неправильного — викидають виняток

```python
def check_positive_assert(number: float) -> float:
    assert number > 0, "Число має бути більшим за нуль!"
    return number

def create_name(name: str) -> str:
    if not name:
        raise ValueError("Ім'я не може бути порожнім")
    return name
```

* **Завдання 2 — Тестування функції підрахунку голосних**
    1. Створили функцію `count_vowels` яка рахує голосні літери у рядку
    2. Написали 6 тестів: для англійських літер, без голосних, порожній рядок, цифри, українські літери

```python
def count_vowels(text: str) -> int:
    vowels = set("aeiouAEIOUаеєиіїоуюяАЕЄИІЇОУЮЯ")
    return sum(1 for ch in text if ch in vowels)
```

* **Завдання 3 — Клас Figure та тести**
    1. Створили клас `Figure` з властивостями `get_figure_type`, `get_figure_length`, `get_angles`
    2. Додали перевірку на нульову та від'ємну довжину, невідомий тип фігури
    3. Використали `setUp` та `tearDown` для підготовки тестового середовища

```python
class Figure:
    VALID_TYPES = ("квадрат", "прямокутник", "трикутник")

    def __init__(self, figure_type: str, length: float):
        if length <= 0:
            raise ValueError("Довжина має бути більшою за нуль")
        if figure_type not in self.VALID_TYPES:
            raise ValueError(f"Невідомий тип фігури: {figure_type}")
        self._figure_type = figure_type
        self._length = length
```

* **Завдання 4 — Тест який спочатку не проходив**

Тест `test_english_vowels` спочатку падав:
```text
FAIL: test_english_vowels
AssertionError: 3 != 2
```
У слові `"apple"` лише 2 голосні (a, e), а не 3. Виправили значення в тесті:
```python
# було
self.assertEqual(3, count_vowels("apple"))

# стало
self.assertEqual(2, count_vowels("apple"))
```
Після виправлення всі тести пройшли.

* **Завдання 5 — subTest**
    1. Використали `subTest` для перевірки кількох наборів даних в одному тесті
    2. Якщо один набір не проходить — видно який саме, інші продовжують виконуватись

```python
def test_figure_lengths_subtest(self):
    for length in [1, 5, 10]:
        with self.subTest(length=length):
            f = Figure("квадрат", length)
            self.assertEqual(length, f.get_figure_length)
```

* **Завдання 6 — Mock**
    1. Створили функцію `ask_user_number` з `input()`
    2. Протестували її через `patch` без ручного введення

```python
@patch("builtins.input", return_value="5")
def test_ask_user_number_returns_value(self, mock_input):
    result = ask_user_number()
    self.assertEqual("5", result)
    mock_input.assert_called_once()
```

* **Команди запуску:**
```text
cd 01_general_and_unittest
python -m unittest test -v
```

* **Результат виконання тестів:**
```text
test_all_vowels ... ok
test_digits_only ... ok
test_empty_string ... ok
test_english_vowels ... ok
test_no_vowels ... ok
test_ukrainian_letters ... ok
test_rectangle_angles ... ok
test_square_angles ... ok
test_triangle_angles ... ok
test_length_is_correct ... ok
test_negative_length_raises ... ok
test_unknown_type_raises ... ok
test_zero_length_raises ... ok
test_all_figure_types_subtest ... ok
test_figure_lengths_subtest ... ok
test_rectangle_type ... ok
test_square_type ... ok
test_triangle_type ... ok
test_ask_user_number_empty ... ok
test_ask_user_number_returns_value ... ok
test_assert_negative_raises ... ok
test_assert_positive_number_ok ... ok
test_assert_zero_raises ... ok
test_create_name_empty_raises ... ok
test_create_name_ok ... ok

Ran 25 tests in 0.003s

OK
```

---
### Висновок:

- В роботі реалізовано юніт-тестування на Python за допомогою бібліотеки `unittest`
- Мету роботи досягнуто — написано 25 тестів для функцій та класу
- Отримано знання про `assert`, `raise ValueError`, `setUp/tearDown`, `subTest`, `mock patch`
- Відповіді на всі питання отримано в ході виконання
- Всі завдання виконано успішно
- Складність виникла з налаштуванням середовища (PATH для pip та git)
- Формат здачі через GitHub зручний і наочний
- Побажання: додати більше прикладів з реальних проєктів
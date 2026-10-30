def check_positive_assert(number: float) -> float:
    assert number > 0, "Число має бути більшим за нуль!"
    return number


def create_name(name: str) -> str:
    if not name:
        raise ValueError("Ім'я не може бути порожнім")
    return name


def count_vowels(text: str) -> int:
    vowels = set("aeiouAEIOUаеєиіїоуюяАЕЄИІЇОУЮЯ")
    return sum(1 for ch in text if ch in vowels)


def ask_user_number() -> str:
    value = input("Введіть число: ")
    return value
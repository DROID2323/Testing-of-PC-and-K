"""Запускає всі кроки лабораторної №03 і формує REPORT.md з реальними результатами.

Використання:
    python make_report.py "Прізвище Ім'я" "Група"
або (poetry):
    poetry run python make_report.py "Прізвище Ім'я" "Група"
"""
import datetime
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
COV = [PY, "-m", "coverage"]
PYTEST = [PY, "-m", "pytest", "-p", "no:cacheprovider"]
OUT = ROOT / "results"

try:
    import coverage
    import pytest
    import pytest_cov  # noqa: F401
except ImportError as exc:
    sys.exit(f"Не вистачає залежності: {exc.name}. Виконайте: pip install coverage pytest pytest-cov")


def sh(args, cwd=ROOT, rcfile=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1", NO_COLOR="1")
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env)
    text = (p.stdout + p.stderr).strip().replace(str(cwd), "<project>").replace(str(ROOT), "<project>").replace(str(ROOT.parent), "<repo>")
    return text, p.returncode


def cov_run(label, runner_args, rcfile=None):
    """erase -> run -> report -m. Повертає (команди, вивід report)."""
    rc = ["--rcfile=" + rcfile] if rcfile else []
    sh(COV + ["erase"])
    run_out, _ = sh(COV + ["run"] + rc + ["-m"] + runner_args)
    rep, _ = sh(COV + ["report"] + rc + ["-m"])
    (OUT / f"{label}.txt").write_text(run_out + "\n\n" + rep + "\n", encoding="utf-8")
    return run_out, rep


def rows(text):
    res = {}
    for line in text.splitlines():
        t = line.split(None, 6)
        if len(t) >= 6 and all(x.isdigit() for x in t[1:5]) and t[5].endswith("%"):
            res[t[0]] = t
    return res


def app_row(text):
    r = rows(text)
    return r.get("TOTAL") or r.get("app.py")


def missing(row):
    lines, branches = [], []
    if row and len(row) >= 7:
        for part in row[6].split(","):
            part = part.strip()
            if "->" in part:
                branches.append(part)
            elif "-" in part:
                a, b = part.split("-")
                lines += range(int(a), int(b) + 1)
            elif part.isdigit():
                lines.append(int(part))
    return lines, branches


def miss_block(rep):
    out, br = [], []
    for f in ("app.py", "validation.py"):
        lines = (ROOT / f).read_text(encoding="utf-8").splitlines()
        row = rows(rep).get(f)
        if not row:
            continue
        ls, bs = missing(row)
        if ls:
            out.append(f"# {f}\n" + "\n".join(f"{n:>3}: {lines[n-1]}" for n in ls if 0 < n <= len(lines)))
        br += [f"{f}: {b}" for b in bs]
    return "\n\n".join(out) or "(немає)", ", ".join(br) or "—"


def fence(text, lang=""):
    return f"```{lang}\n{text}\n```"


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "—"
    group = sys.argv[2] if len(sys.argv) > 2 else "—"
    OUT.mkdir(exist_ok=True)

    # 1. Звичайний запуск тестів
    pytest_v, _ = sh(PYTEST + ["-v"])
    # 2. unittest і pytest окремо
    # беремо лише власний unittest-набір (discover також імпортував би pytest-файли)
    ut_run, ut_rep = cov_run("unittest", ["unittest", "test_unittest", "-v"])
    py_run, py_rep = cov_run("pytest", ["pytest", "-p", "no:cacheprovider", "test_app.py", "test_validation.py"])
    # 3. До / після
    b_run, b_rep = cov_run("before", ["pytest", "-p", "no:cacheprovider", "test_before.py"])
    a_run, a_rep = cov_run("after", ["pytest", "-p", "no:cacheprovider", "test_app.py", "test_validation.py"])
    # 4. pytest-cov
    pc, _ = sh(PYTEST + ["--cov=app", "--cov=validation", "--cov-branch", "--cov-report=term-missing", "-v"])
    # 5. Тест без assert
    w_run, w_rep = cov_run("weak", ["pytest", "-p", "no:cacheprovider", "test_weak.py"])
    # 6. pragma
    np_run, np_rep = cov_run("no_pragma", ["pytest", "-p", "no:cacheprovider", "test_app.py", "test_validation.py"],
                             rcfile=".coveragerc_nopragma")
    # 7. HTML / XML (на повному наборі)
    sh(COV + ["erase"])
    sh(COV + ["run", "-m", "pytest", "-p", "no:cacheprovider", "test_app.py", "test_validation.py"])
    html_out, _ = sh(COV + ["html"])
    xml_out, _ = sh(COV + ["xml"])
    xml_head = "\n".join((ROOT / "coverage.xml").read_text(encoding="utf-8").splitlines()[:14]) \
        if (ROOT / "coverage.xml").exists() else "(coverage.xml не створено)"
    xml_head = xml_head.replace(str(ROOT), "<project>")
    html_files = sorted(p.name for p in (ROOT / "htmlcov").glob("*")) if (ROOT / "htmlcov").exists() else []
    # 8. Пороги
    ok_out, ok_rc = sh(PYTEST + ["test_app.py", "test_validation.py", "--cov=app", "--cov=validation", "--cov-branch", "--cov-fail-under=90"])
    bad_out, bad_rc = sh(PYTEST + ["test_before.py", "--cov=app", "--cov=validation", "--cov-branch", "--cov-fail-under=90"])

    # 9. Мутація: помилка в app.py, яку тест без assert не помічає
    tmp = Path(tempfile.mkdtemp())
    mutated = (ROOT / "app.py").read_text(encoding="utf-8").replace(
        'return 4', 'return 5', 1)
    (tmp / "app.py").write_text(mutated, encoding="utf-8")
    for f in ("test_weak.py", "test_app.py"):
        shutil.copy(ROOT / f, tmp / f)
    shutil.copy(ROOT / "validation.py", tmp / "validation.py")
    mut_weak, mut_weak_rc = sh(PYTEST + ["-q", "test_weak.py"], cwd=tmp)
    mut_strong, mut_strong_rc = sh(PYTEST + ["-q", "test_app.py"], cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)

    tb, ta, tw, tn = app_row(b_rep), app_row(a_rep), app_row(w_rep), app_row(np_rep)

    def tr(label, r):
        return f"| {label} | " + " | ".join(r[1:6]) + " |" if r else f"| {label} | ? | ? | ? | ? | ? |"

    miss_src, bb = miss_block(b_rep)
    nopr_src, _ = miss_block(np_rep)

    md = f"""# Звіт: Покриття коду (Лабораторна робота №03)

**Виконав:** {name}  
**Група:** {group}  
**Дата:** {datetime.date.today():%d.%m.%Y}

## 1. Мета
Навчитися вимірювати покриття коду тестами (`coverage.py`, `pytest-cov`), читати звіт, розрізняти покриття рядків і розгалужень, налаштовувати виключення, формувати HTML/XML-звіти та контролювати поріг покриття у CI.

## 2. Середовище
- Python {platform.python_version()} ({platform.system()})
- coverage {coverage.__version__}, pytest {pytest.__version__}

## 3. Структура проєкту
| Файл | Призначення |
|---|---|
| `app.py` | Клас `Figure` (тип, довжина, `get_angles` з гілками для квадрата, прямокутника, трикутника), `__str__` та `main()` |
| `validation.py` | Допоміжні функції: `check_positive_assert`, `create_name`, `count_vowels`, `ask_user_number` |
| `test_app.py` | pytest-тести класу `Figure` з лабораторної №2 + тест `main()` |
| `test_validation.py` | pytest-тести `validation.py` |
| `test_unittest.py` | Той самий функціонал (`Figure`, `main`, `validation`) на `unittest` |
| `test_before.py` | Початковий стан: протестовано лише трикутник (`Figure`) |
| `test_weak.py` | Тест без жодного `assert` (для розділу «чого coverage не доводить») |
| `.coveragerc` | Налаштування `coverage.py` (`source`, `branch`, `omit`) |
| `.coveragerc_nopragma` | Копія конфігу без виключення `pragma: no cover` — лише для порівняння |
| `.github/workflows/coverage.yml` | CI: тести, `coverage.xml`, поріг 90% |
| `.gitignore` | Службові файли, що не комітяться |
| `make_report.py` | Скрипт, що запускає всі команди й генерує цей звіт |

## 4. Команда запуску тестів
```bash
poetry run pytest -v
```
{fence(pytest_v)}

## 5. Окремі запуски unittest і pytest
Перед кожним вимірюванням виконується `coverage erase`, щоб результати двох наборів не змішувалися в одному файлі `.coverage`.

### unittest
```bash
coverage erase
coverage run -m unittest test_unittest
coverage report -m
```
{fence(ut_rep)}

### pytest
```bash
coverage erase
coverage run -m pytest test_app.py test_validation.py
coverage report -m
```
{fence(py_rep)}

## 6. Покриття до і після додавання тестів
| Етап | Stmts | Miss | Branch | BrPart | Cover |
|---|---|---|---|---|---|
{tr("До (лише трикутник, `test_before.py`)", tb)}
{tr("Після (усі фігури, `test_app.py`)", ta)}

### До змін
```bash
coverage erase
coverage run -m pytest test_before.py
coverage report -m
```
{fence(b_rep)}

Рядки, які було пропущено до змін (стовпець `Missing`):
{fence(miss_src)}
Гілки, що виконувались лише частково (`BrPart`): `{bb}`.

**Пояснення.** Початковий тест перевіряв лише `get_angles` для трикутника, тому в `get_angles` виконувалася тільки гілка `else`, а `return 4` для квадрата й прямокутника — ні. Не виконувалися також гілки помилок у `__init__` (недопустима довжина та тип), `__str__` і тіло `main()`. Модуль `validation.py` взагалі не імпортувався тестами, тому весь його код (`check_positive_assert`, `create_name`, `count_vowels`, `ask_user_number`) показано як непокритий (`source = .` змушує coverage враховувати файли, які не виконувались). Саме ці рядки й гілки опинилися у стовпці `Missing`.

### Після змін
```bash
coverage erase
coverage run -m pytest test_app.py test_validation.py
coverage report -m
```
{fence(a_rep)}

Додано тести: усі типи фігур, неправильний тип і довжина (`ValueError`), `__str__`, `main()` (через `capsys`) та всі функції `validation.py` (включно з `ask_user_number` через `monkeypatch` для `input`). Кожен тест містить `assert`.

## 7. Покриття рядків і покриття розгалужень
- **Line coverage** показує, чи був рядок виконаний хоча б раз.
- **Branch coverage** показує, чи пройшли тести *кожен напрямок* умовного переходу: і `True`, і `False`.
- Рядок із `if` може бути виконаний (line coverage зарахує його), але якщо умова ніколи не була хибною, стовпець `BrPart` покаже недопокриту гілку. Тому `branch = true` дає точнішу картину.
- У таблицях вище `Stmts`/`Miss` — це рядки, `Branch`/`BrPart` — розгалуження, `Missing` — номери проблемних рядків і переходи виду `a->b`.

### Запуск через pytest-cov
```bash
pytest --cov=app --cov=validation --cov-branch --cov-report=term-missing -v
```
{fence(pc)}

## 8. Межі вимірювання та виключення
Налаштування у `.coveragerc`:
```ini
{(ROOT / ".coveragerc").read_text(encoding="utf-8").strip()}
```
- `source = .` — вимірюється код у поточній папці прикладу (для більшого проєкту вказують каталог пакета, напр. `src/my_app`).
- `branch = true` — вмикає покриття розгалужень.
- `omit` — виключає зі звіту тести, `__init__.py`, віртуальне середовище та службовий `make_report.py`. Сам `app.py` не виключається, тож у звіті є лише код програми (тестових файлів у таблиці немає).

### `pragma: no cover`
У `app.py` позначено точку входу скрипта:
```python
if __name__ == "__main__":  # pragma: no cover
    main()
```
Порівняння з виміром, де виключення вимкнено (`.coveragerc_nopragma`):

| Варіант | Stmts | Miss | Branch | BrPart | Cover |
|---|---|---|---|---|---|
{tr("З `pragma: no cover`", ta)}
{tr("Без `pragma: no cover`", tn)}

Без pragma пропущеними стають рядки:
{fence(nopr_src)}

**Обґрунтування.** Блок `if __name__ == "__main__":` виконується лише при прямому запуску скрипта, а не при імпорті з тестів, тож він не є частиною тестованої поведінки. Бізнес-логіка (`get_angles`) повністю покрита тестами й не виключається, тому pragma не приховує жодної важливої логіки, а лише прибирає службовий рядок зі звіту. Використовувати його для штучного підвищення відсотка не можна.

## 9. HTML- та XML-звіти
```bash
coverage html   # -> htmlcov/index.html
coverage xml    # -> coverage.xml
```
Згенеровані файли `htmlcov/`: {", ".join(f"`{f}`" for f in html_files[:8]) or "—"}{" …" if len(html_files) > 8 else ""}

Початок `coverage.xml`:
{fence(xml_head, "xml")}

- **HTML** призначений для людини: у браузері (`htmlcov/index.html`) видно файли та рядки, підсвічені як покриті, непокриті й частково покриті гілки.
- **XML** призначений для інструментів: CI-системи та сервіси аналізу покриття (Codecov тощо) читають його автоматично.

Згідно з вимогами, самі `htmlcov/` та `coverage.xml` не комітяться (див. `.gitignore`), а в репозиторії лишаються текстові результати у папці `results/`.

## 10. Чого coverage не доводить
Тест `test_weak.py` викликає всі гілки, але не містить жодного `assert`:
```python
def test_weak_calls_everything():
    for kind in ("квадрат", "прямокутник", "трикутник"):
        f = Figure(kind, 5)
        f.get_angles
        ...
    main()
    count_vowels("Привіт")   # результат ніде не перевіряється
```
```bash
coverage erase
coverage run -m pytest test_weak.py
coverage report -m
```
{fence(w_rep)}

Порівняння наборів:

| Набір | Stmts | Miss | Branch | BrPart | Cover |
|---|---|---|---|---|---|
{tr("Без assert (`test_weak.py`)", tw)}
{tr("З assert (`test_app.py`)", ta)}

Покриття однакове (або майже), але гарантії різні. Щоб це довести, у копії `app.py` навмисно внесено помилку: для квадрата `get_angles` повертає 5 замість 4.

- Тести без `assert`: код завершення **{mut_weak_rc}** (0 = усе «пройшло»):
{fence(mut_weak)}
- Тести з `assert`: код завершення **{mut_strong_rc}** (не 0 = помилку виявлено):
{fence(mut_strong)}

**Чому 100% line coverage не означає відсутності помилок.** Покриття лише фіксує, що рядок було виконано. Воно не перевіряє, чи результат правильний. Тест без `assert` виконує код і збільшує відсоток, але пропустить неправильне значення (як у досліді вище). Крім того, покриття не знає про вхідні дані, яких тести не пробували, і про логіку, якої в коді немає взагалі.

## 11. Поріг покриття і CI
```bash
pytest test_app.py test_validation.py --cov=app --cov=validation --cov-branch --cov-fail-under=90
```
Код завершення: **{ok_rc}**
{fence(ok_out)}

Для початкового набору (лише трикутник) той самий поріг не досягається, код завершення: **{bad_rc}**
{fence(bad_out)}

У GitHub Actions (`.github/workflows/coverage.yml`) виконується
`pytest --cov=app --cov=validation --cov-branch --cov-report=xml --cov-report=term-missing --cov-fail-under=90`,
`coverage.xml` завантажується як артефакт, а якщо поріг не досягнуто, джоб завершується невдачею.

## 12. `.gitignore`
```
{(ROOT / ".gitignore").read_text(encoding="utf-8").strip()}
```

## 13. Висновки
1. Покриття показує, які рядки й гілки було виконано; до додавання тестів частина гілок `get_angles` та `main()` лишалася непокритою.
2. Branch coverage строгіший за line coverage: він виявляє недопокриті напрямки умов.
3. Для чистих вимірів потрібно робити `coverage erase` перед кожним запуском.
4. `pragma: no cover` доречний лише для службового коду (точка входу), не для логіки.
5. HTML-звіт зручний людині, XML — інструментам CI.
6. Високий відсоток не гарантує якості: без `assert` тести не виявляють помилок, що показав дослід із мутацією.
7. Поріг `--cov-fail-under` у CI автоматично зупиняє злиття коду з недостатнім покриттям.
"""
    (ROOT / "REPORT.md").write_text(md, encoding="utf-8")
    print("Готово: REPORT.md і папка results/ створені.")


if __name__ == "__main__":
    main()

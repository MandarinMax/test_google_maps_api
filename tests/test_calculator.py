import pytest
from src.calculator import add, divide
import sys

@pytest.mark.smoke
def test_add():
    assert add(2, 3) == 5

@pytest.mark.regression
def test_divide():
    assert divide(10, 2) == 5

@pytest.mark.regression
def test_divide_by_zero_raises_value_error_with_message():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    assert "Нельзя делить на ноль" in str(excinfo.value)

@pytest.mark.slow
def test_very_slow_calculation():
    """Гипотетический тест, который работает очень долго."""
    # для примера просто сделаем его успешным
    assert True

@pytest.mark.skip(reason="Эта функциональность будет реализована в версии 2.0")
def test_subtraction():
    """Тест для будущей функции вычитания."""
    #assert sutract(10,5) == 5
    pass

@pytest.mark.skipif(sys.version_info > (3, 10), reason="Требуется Python 3.10 или выше")
def test_new_python_feature():
    """Тест использующий синтаксисЮ доступный только в новых версиях python 3.10"""
    # Пример использования match-case, который появляется в 3.10
    result = 0
    match 1:
        case 1:
            result = 1
    assert result == 1

@pytest.mark.xfail(reason="Известный баг с точностью float, будет исправлен в task-1")
def test_add_floats_bug():
    # Этот тест будет падать из-за особенностей пердставления float в Python
    assert add(0.1, 0.2) == 0.3

@pytest.mark.parametrize('a, b, expected', [
    # 1. Тест-кейс: Положительные числа
    (1, 2, 3),

    # 2. Тест-кейс: Отрицательные числа
    (-5, -3, -8),

    # 3. Тест-кейс: Смешанные знаки
    (-10, 5, -5),

    # 4. Тест-кейс: Сложение с нулем
    (100, 0, 100),

    # 5. Тест-кейс: Дробные числа (float)
    (0.1, 0.2, 0.3)
])
def test_add_parametrized(a, b, expected):
    """
    Проверяет функцию add на различных наборах данных
    с помощью параметризации.
    """
    # Мы используем approx для сравнения float, чтобы избежать проблем с точностью
    assert add(a, b) == pytest.approx(expected)
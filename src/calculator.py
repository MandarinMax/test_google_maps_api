def add(a, b):
    # ... (код функции add) ...
    return a + b


def divide(a, b):
    """
        Эта функция делит a на b.
        Вызывает ValueError при делении на ноль.
    """
    if b == 0:
        raise ValueError("Нельзя делить на ноль")
    return a / b

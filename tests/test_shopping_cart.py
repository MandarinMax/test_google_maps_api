import pytest

class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, price):
        self.items[item_name] = price

    def get_total_price(self):
        return sum(self.items.values())

@pytest.fixture()
def filled_cart():
    """Создаем и возвращаем корзину с двумя товарами."""
    cart = ShoppingCart()
    cart.add_item("apple", price=10)
    cart.add_item("banana", price=20)
    return cart

def test_add_item(filled_cart):
    filled_cart.add_item("cherry", price=30)
    assert "cherry" in filled_cart.items

def test_get_total_price(filled_cart):
    assert filled_cart.get_total_price() == 30
from app.services.payments import MockPaymentProvider
from app.services.inventory import reserve_product, release_product

class Product:
    stock = 10

def test_inventory_reservation():
    p = Product()
    assert reserve_product(None, p, 4) == 6
    assert release_product(p, 2) == 8

def test_payment_adapter():
    result = MockPaymentProvider().create_payment(100, "SAR", 7)
    assert result.success is True
    assert result.reference == "MOCK-7"

import os
os.environ["DATABASE_URL"] = "sqlite:///./v21_test.db"
from app.services.payments_v20 import sign_payload, verify_signature
from app.services.inventory_v20 import reserve_stock
from app.models import Product

def test_webhook_signature_roundtrip():
    body = b'{"event":"payment.succeeded"}'
    sig = sign_payload("secret", body)
    assert verify_signature("secret", body, sig)
    assert not verify_signature("wrong", body, sig)

def test_inventory_service_rejects_invalid_quantity():
    class DB:
        pass
    try:
        reserve_stock(DB(), 1, 0)
        assert False, "expected ValueError"
    except ValueError:
        pass

def test_v20_product_model_has_stock():
    assert hasattr(Product, "stock")

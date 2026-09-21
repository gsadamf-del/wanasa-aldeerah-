import hashlib, hmac, json
from dataclasses import dataclass
from .payments import PaymentProvider, PaymentResult

@dataclass
class WebhookVerification:
    valid: bool
    event_id: str

def sign_payload(secret: str, raw_body: bytes) -> str:
    return hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()

def verify_signature(secret: str, raw_body: bytes, signature: str) -> bool:
    expected = sign_payload(secret, raw_body)
    return hmac.compare_digest(expected, signature.strip())

class MockPaymentProviderV20(PaymentProvider):
    def create_payment(self, amount: float, currency: str, order_id: int) -> PaymentResult:
        return PaymentResult(True, "mock-v20", f"MOCKV20-{order_id}", "sandbox payment")

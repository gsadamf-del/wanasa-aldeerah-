from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class PaymentResult:
    success: bool
    provider: str
    reference: str | None = None
    message: str | None = None

class PaymentProvider(ABC):
    @abstractmethod
    def create_payment(self, amount: float, currency: str, order_id: int) -> PaymentResult:
        raise NotImplementedError

class MockPaymentProvider(PaymentProvider):
    def create_payment(self, amount: float, currency: str, order_id: int) -> PaymentResult:
        return PaymentResult(
            success=True,
            provider="mock",
            reference=f"MOCK-{order_id}",
            message="payment foundation",
        )

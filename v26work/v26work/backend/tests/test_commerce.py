from app.services.commerce import can_transition
def test_order_flow():
    assert can_transition("PENDING","CONFIRMED")
    assert can_transition("CONFIRMED","PREPARING")
    assert can_transition("PREPARING","READY")
    assert can_transition("READY","OUT_FOR_DELIVERY")
    assert can_transition("OUT_FOR_DELIVERY","DELIVERED")
    assert not can_transition("DELIVERED","PENDING")

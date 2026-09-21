from datetime import date

def expiry_state(expiry_date, today=None):
    if expiry_date is None:
        return "not_applicable"
    today = today or date.today()
    days = (expiry_date - today).days
    if days < 0:
        return "expired"
    if days <= 15:
        return "spot"
    if days <= 60:
        return "liquidation"
    return "normal"

def sellable(expiry_date, today=None):
    return expiry_state(expiry_date, today) != "expired"

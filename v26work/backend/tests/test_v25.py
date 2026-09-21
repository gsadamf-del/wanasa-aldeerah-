from app.services.providers_v25 import StripeProviderV25
from app.services.production_v23 import validate_production_settings
from app.services.restore_v25 import run_restore_drill
from app.core.config import Settings


def test_stripe_signature_roundtrip():
    secret='s'*40
    body=b'{"id":"evt_1"}'
    import time, hmac, hashlib
    ts=str(int(time.time()))
    sig=hmac.new(secret.encode(),f'{ts}.'.encode()+body,hashlib.sha256).hexdigest()
    assert StripeProviderV25.verify_webhook(secret,body,f't={ts},v1={sig}')


def test_production_requires_real_integrations():
    s=Settings(environment='production', jwt_secret_key='j'*40, payment_webhook_secret='p'*40, cors_origins='https://app.example', payment_provider='stripe')
    errors=validate_production_settings(s)
    assert any('STRIPE_SECRET_KEY' in x for x in errors)
    assert any('EXTERNAL_MONITORING_URL' in x for x in errors)


def test_restore_drill_missing_binary_is_safe():
    result=run_restore_drill('/nonexistent.backup','postgresql://invalid')
    assert result['status'] in {'NOT_RUN','FAILED'}

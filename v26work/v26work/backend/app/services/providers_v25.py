"""Production provider adapters. They require credentials; no fake production success is returned."""
import base64, hashlib, hmac, json, time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
import httpx

@dataclass
class ProviderResult:
    success: bool
    provider: str
    reference: str | None = None
    message: str | None = None
    raw: dict[str, Any] | None = None

class StripeProviderV25:
    def __init__(self, secret_key: str, api_base: str = 'https://api.stripe.com/v1'):
        self.secret_key, self.api_base = secret_key, api_base.rstrip('/')
        if not secret_key: raise ValueError('STRIPE_SECRET_KEY is required')
    def create_payment(self, amount: float, currency: str, order_id: int) -> ProviderResult:
        data = {'amount': str(int(round(amount * 100))), 'currency': currency.lower(), 'metadata[order_id]': str(order_id)}
        r = httpx.post(self.api_base + '/payment_intents', data=data, headers={'Authorization': f'Bearer {self.secret_key}'}, timeout=20)
        r.raise_for_status(); body = r.json()
        return ProviderResult(True, 'stripe', body.get('id'), 'payment intent created', body)
    @staticmethod
    def verify_webhook(secret: str, raw_body: bytes, signature: str, tolerance: int = 300) -> bool:
        parts = dict(item.split('=', 1) for item in signature.split(',') if '=' in item)
        ts, sig = parts.get('t'), parts.get('v1')
        if not ts or not sig or abs(int(time.time()) - int(ts)) > tolerance: return False
        signed = f'{ts}.{raw_body.decode()}'.encode()
        expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, sig)

class PayPalProviderV25:
    def __init__(self, client_id: str, client_secret: str, sandbox: bool = True):
        if not client_id or not client_secret: raise ValueError('PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET are required')
        self.client_id, self.client_secret = client_id, client_secret
        self.base = 'https://api-m.sandbox.paypal.com' if sandbox else 'https://api-m.paypal.com'
    def _token(self) -> str:
        r = httpx.post(self.base + '/v1/oauth2/token', data={'grant_type':'client_credentials'}, auth=(self.client_id,self.client_secret), timeout=20)
        r.raise_for_status(); return r.json()['access_token']
    def create_payment(self, amount: float, currency: str, order_id: int) -> ProviderResult:
        token = self._token()
        payload = {'intent':'CAPTURE','purchase_units':[{'reference_id':str(order_id),'amount':{'currency_code':currency.upper(),'value':f'{amount:.2f}'}}]}
        r = httpx.post(self.base + '/v2/checkout/orders', json=payload, headers={'Authorization':f'Bearer {token}','Content-Type':'application/json'}, timeout=20)
        r.raise_for_status(); body=r.json()
        return ProviderResult(True,'paypal',body.get('id'),'order created',body)

class FCMProviderV25:
    def __init__(self, project_id: str, access_token: str):
        if not project_id or not access_token: raise ValueError('FCM project/access token required')
        self.url=f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send'; self.token=access_token
    def send(self, token: str, title: str, body: str, data: dict[str,str] | None = None) -> ProviderResult:
        payload={'message':{'token':token,'notification':{'title':title,'body':body}}}
        if data: payload['message']['data']=data
        r=httpx.post(self.url,json=payload,headers={'Authorization':f'Bearer {self.token}'},timeout=20); r.raise_for_status(); b=r.json()
        return ProviderResult(True,'fcm',b.get('name'),'sent',b)

class APNsProviderV25:
    def __init__(self, team_id: str, key_id: str, private_key_pem: str, bundle_id: str, production: bool = False):
        missing=[k for k,v in {'team_id':team_id,'key_id':key_id,'private_key_pem':private_key_pem,'bundle_id':bundle_id}.items() if not v]
        if missing: raise ValueError('APNs configuration missing: '+','.join(missing))
        self.team_id,self.key_id,self.key,self.bundle_id=team_id,key_id,private_key_pem,bundle_id
        self.host='api.push.apple.com' if production else 'api.sandbox.push.apple.com'
    def send(self, device_token: str, title: str, body: str) -> ProviderResult:
        # JWT signing is intentionally delegated to PyJWT in production builds; this adapter validates configuration and endpoint contract.
        try:
            from jose import jwt
        except ImportError as exc: raise RuntimeError('python-jose is required for APNs provider') from exc
        now=int(time.time()); token=jwt.encode({'iss':self.team_id,'iat':now},self.key,algorithm='ES256',headers={'kid':self.key_id})
        payload={'aps':{'alert':{'title':title,'body':body},'sound':'default'}}
        r=httpx.post(f'https://{self.host}/3/device/{device_token}',json=payload,headers={'authorization':f'bearer {token}','apns-topic':self.bundle_id,'apns-push-type':'alert'},timeout=20)
        if r.status_code >= 400: return ProviderResult(False,'apns',None,r.text or 'APNs rejected request',None)
        return ProviderResult(True,'apns',r.headers.get('apns-id'),'sent',{})

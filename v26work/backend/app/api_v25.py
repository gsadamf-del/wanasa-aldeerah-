from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .db.session import get_db
from .rbac import require_roles
from .core.config import settings
from .services.monitoring_v25 import ExternalMonitoringV25, monitoring

router = APIRouter(prefix='/api/v25', tags=['v25'])

@router.get('/health')
def health(): return {'status':'ok','service':'wanasa-aldeerah','version':'26'}

@router.get('/readiness')
def readiness(db: Session = Depends(get_db)):
    from sqlalchemy import text
    db.execute(text('SELECT 1'))
    return {'ready': True, 'database':'ok', 'version':'26', 'external_monitoring': bool(settings.external_monitoring_url)}

@router.get('/capabilities')
def capabilities():
    return {'version':'26','release':'production-integration-v26','payments':['stripe','paypal'],'notifications':['fcm','apns'],'external_monitoring':bool(settings.external_monitoring_url),'restore_drills':True,'android':True,'ios':True}

@router.post('/admin/monitoring/test')
def monitoring_test(user=Depends(require_roles('admin'))):
    ok=ExternalMonitoringV25(settings.external_monitoring_url, settings.external_monitoring_api_key).emit('wanasa_v25_monitoring_test', severity='info')
    return {'sent':ok,'configured':bool(settings.external_monitoring_url)}

from decimal import Decimal
from pydantic import BaseModel
from .models import Order
from .models_v19 import Payment, DeviceToken
from .services.provider_factory_v25 import payment_provider, push_providers
from .rbac import current_user

class PaymentCreateV25(BaseModel):
    order_id: int
    currency: str = 'SAR'

@router.post('/payments')
def create_payment_v25(payload: PaymentCreateV25, db: Session = Depends(get_db), user=Depends(current_user)):
    order=db.get(Order,payload.order_id)
    if not order or order.customer_id != user.id: raise HTTPException(404,'order not found')
    try:
        provider=payment_provider(settings)
        result=provider.create_payment(float(order.total), payload.currency, order.id)
    except Exception as exc:
        monitoring.emit('payment_provider_error', severity='error', provider=settings.payment_provider, error=type(exc).__name__)
        raise HTTPException(502, f'payment provider unavailable: {type(exc).__name__}')
    payment=Payment(order_id=order.id, amount=Decimal(order.total), currency=payload.currency, provider=result.provider, status='PENDING' if result.success else 'FAILED', reference=result.reference)
    db.add(payment); db.commit(); db.refresh(payment)
    return {'payment_id':payment.id,'status':payment.status,'provider':result.provider,'reference':result.reference,'message':result.message}

class PushTestV25(BaseModel):
    user_id: int
    title: str
    body: str

@router.post('/admin/push/test')
def push_test(payload: PushTestV25, db: Session = Depends(get_db), user=Depends(require_roles('admin'))):
    devices=db.query(DeviceToken).filter_by(user_id=payload.user_id, active=True).all()
    providers=push_providers(settings)
    if not providers: raise HTTPException(503,'no FCM/APNs provider configured')
    results=[]
    for device in devices:
        for provider in providers:
            is_fcm=provider.__class__.__name__.startswith('FCM')
            if (device.platform == 'android' and not is_fcm) or (device.platform == 'ios' and is_fcm):
                continue
            try:
                r=provider.send(device.token,payload.title,payload.body)
                results.append({'provider':r.provider,'success':r.success,'reference':r.reference})
            except Exception as exc: results.append({'provider':provider.__class__.__name__,'success':False,'error':type(exc).__name__})
    return {'devices':len(devices),'results':results}

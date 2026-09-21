from .providers_v25 import StripeProviderV25, PayPalProviderV25, FCMProviderV25, APNsProviderV25

def payment_provider(settings):
    name=settings.payment_provider.lower()
    if name == 'stripe': return StripeProviderV25(settings.stripe_secret_key)
    if name == 'paypal': return PayPalProviderV25(settings.paypal_client_id, settings.paypal_client_secret, settings.paypal_sandbox)
    raise ValueError(f'Unsupported production payment provider: {name}')

def push_providers(settings):
    result=[]
    if settings.fcm_project_id and settings.fcm_access_token: result.append(FCMProviderV25(settings.fcm_project_id, settings.fcm_access_token))
    if settings.apns_team_id and settings.apns_key_id and settings.apns_private_key: result.append(APNsProviderV25(settings.apns_team_id,settings.apns_key_id,settings.apns_private_key,settings.apns_bundle_id,settings.apns_production))
    return result

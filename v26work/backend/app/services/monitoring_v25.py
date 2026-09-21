import json, logging, os, time
from urllib.request import Request, urlopen

class ExternalMonitoringV25:
    def __init__(self, endpoint: str | None = None, api_key: str | None = None):
        self.endpoint, self.api_key = endpoint, api_key
    def emit(self, event: str, severity: str='info', **fields):
        payload={'event':event,'severity':severity,'timestamp':time.time(),**fields}
        logging.getLogger('wanasa.monitoring').info(json.dumps(payload,separators=(',',':')))
        if not self.endpoint: return False
        req=Request(self.endpoint,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json',**({'Authorization':f'Bearer {self.api_key}'} if self.api_key else {})},method='POST')
        try:
            with urlopen(req, timeout=5) as r: return 200 <= r.status < 300
        except Exception:
            return False

monitoring = ExternalMonitoringV25(os.getenv('EXTERNAL_MONITORING_URL'), os.getenv('EXTERNAL_MONITORING_API_KEY'))

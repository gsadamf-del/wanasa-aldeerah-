from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app import models, models_v19, models_v20, models_v21, models_v22, models_v23, models_v24, models_v25  # noqa: F401
from app.api import router
from app.api_v18 import router as v18_router
from app.api_v19 import router as v19_router
from app.api_v20 import router as v20_router
from app.api_v21 import router as v21_router
from app.api_v22 import router as v22_router
from app.api_v23 import router as v23_router
from app.api_v24 import router as v24_router
from app.api_v25 import router as v25_router
from app.services.production_v23 import InMemoryRateLimiterV23, validate_production_settings
from sqlalchemy import text
from sqlalchemy import text
import logging, json, time

app = FastAPI(title="Wanasa Al Deerah API", version="26.0.0")
EXPECTED_DB_REVISION = "202609220001"

origins = ["*"] if settings.cors_origins == "*" else [x.strip() for x in settings.cors_origins.split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

limiter = InMemoryRateLimiterV23(settings.rate_limit_requests, settings.rate_limit_window_seconds)
logger = logging.getLogger("wanasa")

@app.middleware("http")
async def v23_production_middleware(request, call_next):
    import uuid
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    client_key = request.client.host if request.client else "unknown"
    allowed, retry_after = limiter.allow(client_key)
    if not allowed and request.url.path not in {"/api/v23/health", "/api/v23/readiness"}:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=429, content={"detail":"rate limit exceeded", "request_id":request_id}, headers={"Retry-After":str(retry_after), "X-Request-Id":request_id})
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    logger.info(json.dumps({"event":"http_request","request_id":request_id,"method":request.method,"path":request.url.path,"status":response.status_code,"duration_ms":round((time.perf_counter()-started)*1000,2)}, separators=(",",":")))
    return response

startup_config_errors = validate_production_settings(settings)
if startup_config_errors and settings.environment.lower() in {"production", "prod"}:
    raise RuntimeError("Invalid production configuration: " + "; ".join(startup_config_errors))

# V26 release gate: production databases MUST have the expected Alembic revision.
def verify_production_schema() -> None:
    if settings.environment.lower() not in {"production", "prod"}:
        Base.metadata.create_all(bind=engine)
        return
    with engine.connect() as connection:
        revision = connection.execute(text("SELECT version_num FROM alembic_version LIMIT 1")).scalar()
        if revision != EXPECTED_DB_REVISION:
            raise RuntimeError(f"Database migration required: expected {EXPECTED_DB_REVISION}, found {revision!r}")

verify_production_schema()

app.include_router(router)
app.include_router(v18_router)
app.include_router(v19_router)
app.include_router(v20_router)
app.include_router(v21_router)
app.include_router(v22_router)
app.include_router(v23_router)
app.include_router(v24_router)
app.include_router(v25_router)

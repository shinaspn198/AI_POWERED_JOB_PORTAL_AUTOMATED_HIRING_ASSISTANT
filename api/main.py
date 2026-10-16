from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.resume import router as resume_router
from api.routes.scoring import router as scoring_router
from api.routes.shortlisting import router as shortlisting_router
from api.routes.jobs import router as jobs_router
from api.routes.assessment import router as assessment_router
from api.routes.integration import router as integration_router
from api.errors import api_error_handler
from api.logger import logger
from api.routes.auth import router as auth_router

from api.routes.monitoring import router as monitoring_router
from performance.ai_monitoring import ai_monitor
import time
from fastapi import Request

app = FastAPI(
    title="Zecpath AI ATS API",
    description="API layer for the Zecpath AI recruitment system",
    version="1.0.0"
)

@app.middleware("http")
async def monitor_requests_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500
    err_str = None
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception as exc:
        err_str = str(exc)
        raise exc
    finally:
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        ai_monitor.log_api_request(
            method=request.method,
            endpoint=request.url.path,
            status_code=status_code,
            latency_ms=latency_ms,
            error=err_str
        )

app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Zecpath AI ATS API started")

app.add_exception_handler(
    Exception,
    api_error_handler
)

app.include_router(resume_router)
app.include_router(scoring_router)
app.include_router(shortlisting_router)
app.include_router(jobs_router)
app.include_router(assessment_router)
app.include_router(integration_router)
app.include_router(monitoring_router)


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Zecpath AI ATS API is running"
    }
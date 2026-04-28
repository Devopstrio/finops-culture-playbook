import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("finops-culture-playbook-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="FinOps Culture Playbook API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/billing/summary")
def get_billing_summary():
    return {
        "mtd_spend": 450000.0,
        "forecast_spend": 475000.0,
        "savings_mtd": 12000.0,
        "anomalies_detected": 2
    }

@app.get("/costs/by-team")
def get_costs_by_team():
    return [
        {"team": "Retail App", "spend": 120000, "budget": 100000, "efficiency": 0.82},
        {"team": "Markets Platform", "spend": 85000, "budget": 90000, "efficiency": 0.94},
        {"team": "Data Science", "spend": 45000, "budget": 40000, "efficiency": 0.78}
    ]

@app.post("/forecast/run")
def run_forecast(days: int = 30):
    logger.info(f"Running spend forecast for next {days} days")
    return {"status": "RUNNING", "job_id": f"forecast_{int(time.time())}", "target_days": days}

@app.get("/commitments/summary")
def get_commitments_summary():
    return {
        "ri_coverage": 0.84,
        "savings_plan_coverage": 0.62,
        "on_demand_pct": 0.24,
        "optimization_opportunity": 15000.0
    }

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "maturity_score": 72,
        "accountability_score": 0.65,
        "optimization_score": 0.88,
        "value_realization": 0.74
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_active_teams": 42,
        "open_anomalies": 1,
        "last_sync": "2026-04-28T10:00:00Z",
        "maestro_status": "READY"
    }

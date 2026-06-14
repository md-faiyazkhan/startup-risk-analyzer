import logging
import time
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field
from typing import Literal
import uvicorn
from app.predictor import predict_risk

# Track server start time
START_TIME = time.time()

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI instance
app = FastAPI(
    title="Startup Risk Analyzer API",
    description="Predicts startup success or failure based on key business metrics.",
    version="v1.0"
)

# Input Schema
class StartupInput(BaseModel):
    funding_rounds: int = Field(..., ge=0, le=8, description="Number of funding rounds")
    founder_experience_years: int = Field(..., ge=0, le=24, description="Years of founder experience")
    team_size: int = Field(..., ge=2, le=299, description="Total team members")
    market_size_billion: float = Field(..., gt=0, description="Market size in billion USD")
    product_traction_users: int = Field(..., ge=0, description="Number of active users")
    burn_rate_million: float = Field(..., gt=0, description="Monthly burn rate in million USD")
    revenue_million: float = Field(..., ge=0, description="Monthly revenue in million USD")
    investor_type: Literal['angel', 'none', 'tier1_vc', 'tier2_vc'] = Field(..., description="Type of investor")
    sector: Literal['AI', 'Climate', 'Crypto', 'Ecommerce', 'Fintech', 'Health', 'SaaS'] = Field(..., description="Industry sector")
    founder_background: Literal['academic', 'ex_bigtech', 'first_time', 'serial_founder'] = Field(..., description="Founder background")

# API Router with v1 prefix
router = APIRouter(prefix="/v1")

# Health Check Endpoint
@router.get("/health")
def health():
    uptime = round(time.time() - START_TIME, 2)
    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "model": "loaded",
        "version": "v1.0",
        "uptime_seconds": uptime
    }

# Prediction Endpoint
@router.post("/predict")
def predict(data: StartupInput):
    logger.info(f"Prediction requested — sector: {data.sector}, investor_type: {data.investor_type}")
    start_time = time.time()
    try:
        input_dict = data.model_dump()
        result = predict_risk(input_dict)
        response_time = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Prediction result — risk_category: {result['risk_category']}, success_probability: {result['success_probability']}%, response_time: {response_time}ms")
        return result
    except Exception as e:
        response_time = round((time.time() - start_time) * 1000, 2)
        logger.error(f"Prediction failed — error: {str(e)}, response_time: {response_time}ms")
        raise HTTPException(status_code=500, detail=str(e))

# Register router with app
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
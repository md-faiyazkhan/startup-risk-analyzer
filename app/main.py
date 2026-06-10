from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
from app.predictor import predict_risk

# FastAPI instance
app = FastAPI(
    title="Startup Risk Analyzer API",
    description="Predicts startup success or failure based on key business metrics.",
    version="1.0.0"
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
    investor_type: str = Field(..., description="Type of investor: angel, none, tier1_vc, tier2_vc")
    sector: str = Field(..., description="Industry sector")
    founder_background: str = Field(..., description="Founder background")

# Health Check Endpoint
@app.get("/")
def root():
    return {"message": "Startup Risk Analyzer API is running"}

# Prediction Endpoint
@app.post("/predict")
def predict(data: StartupInput):
    try:
        input_dict = data.model_dump()
        result = predict_risk(input_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    
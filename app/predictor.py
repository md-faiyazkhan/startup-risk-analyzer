import numpy as np
import pandas as pd
import joblib

# Load final pipeline
pipeline = joblib.load('../models/final_pipeline.joblib')

def engineer_features(data:dict) -> pd.DataFrame:
    """
    Applies the same feature engineering as training piepline.
    """
    burn_rate = data['burn_rate_million']
    revenue = data['revenue_million']
    team = data['team_size']
    traction = data['product_traction_users']

    # Feature Engineering - same as training
    data['burn_efficiency'] = revenue / burn_rate if burn_rate != 0 else 0
    data['revenue_per_employee'] = revenue / team if team != 0 else 0 
    data['traction_per_employee'] = traction / team if team != 0 else 0 
    data['runway_risk'] = 1 if burn_rate > revenue else 0

    return pd.DataFrame([data]) 


def predict_risk(data: dict) -> dict:
    """
    Takes startup data, runs prediction, returns risk assessment.
    """
    # Prepare input
    input_df = engineer_features(data)

    # Prediction
    prediction = pipeline.predict(input_df)[0]
    probability = pipeline.predict_proba(input_df)[0]

    failure_prob = round(float(probability[0]) * 100, 2)
    success_prob = round(float(probability[1]) * 100, 2)

    # Risk Category
    if success_prob >= 75:
        risk_category = "Low Risk"
    elif success_prob >= 50:
        risk_category = "Medium Risk"
    else:
        risk_category = "High Risk"

    return {
        "prediction": int(prediction),
        "success_probability": success_prob,
        "failure_probability": failure_prob,
        "risk_category": risk_category
    }


from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

# Create a test client
client = TestClient(app)


# Valid sample payload used across multiple test cases
sample_payload = {
    "funding_rounds": 3,
    "founder_experience_years": 5,
    "team_size": 20,
    "market_size_billion": 10.5,
    "product_traction_users": 5000,
    "burn_rate_million": 0.5,
    "revenue_million": 1.0,
    "investor_type": "tier1_vc",
    "sector": "fintech",
    "founder_background": "technical"
}


# Test successful prediction response
@patch("app.main.predict_risk")
def test_predict_success(mock_predict):
    """
    Verify that the /predict endpoint returns the expected
    response when prediction is successful.
    """

    # Mock the prediction function's return value
    mock_predict.return_value = {
        "prediction": 1,
        "success_probability": 80.0,
        "failure_probability": 20.0,
        "risk_category": "Low Risk"
    }

    # Send POST request to the prediction endpoint
    response = client.post("/predict", json=sample_payload)

    # Verify HTTP status code
    assert response.status_code == 200

    # Parse response JSON
    response_data = response.json()

    # Verify response content
    assert response_data["prediction"] == 1
    assert response_data["success_probability"] == 80.0
    assert response_data["failure_probability"] == 20.0
    assert response_data["risk_category"] == "Low Risk"

    # Verify that predict_risk() was called exactly once
    mock_predict.assert_called_once()


# Test request validation for invalid input data
def test_predict_invalid_input():
    """
    Verify that FastAPI returns a 422 validation error
    when invalid input is provided.
    """

    # Invalid payload: funding_rounds cannot be negative
    invalid_payload = {
        "funding_rounds": -1,
        "founder_experience_years": 5,
        "team_size": 20,
        "market_size_billion": 10.5,
        "product_traction_users": 5000,
        "burn_rate_million": 0.5,
        "revenue_million": 1.0,
        "investor_type": "tier1_vc",
        "sector": "fintech",
        "founder_background": "technical"
    }

    # Send POST request with invalid data
    response = client.post("/predict", json=invalid_payload)

    # Verify validation error status code
    assert response.status_code == 422


# Test internal server error handling
@patch("app.main.predict_risk")
def test_predict_internal_server_error(mock_predict):
    """
    Verify that the /predict endpoint returns a 500 error
    when an unexpected exception occurs.
    """

    # Simulate an exception in the prediction function
    mock_predict.side_effect = Exception("Model failed")

    # Send POST request
    response = client.post("/predict", json=sample_payload)

    # Verify HTTP status code
    assert response.status_code == 500

    # Verify error response
    assert response.json() == {
        "detail": "Model failed"
    }

    # Verify that predict_risk() was called exactly once
    mock_predict.assert_called_once()




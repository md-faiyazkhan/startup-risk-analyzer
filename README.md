# 🚀 Startup Risk Analyzer

Predicts whether a startup will succeed or fail based on key business metrics — built as a complete end-to-end Machine Learning system.

---

<!-- ## 🌐 Live Demo

| Service | URL |
|---------|-----|
| Streamlit Dashboard | [Coming Soon] |
| FastAPI Documentation | [Coming Soon] | -->

---

## 📌 Problem Statement

Every year, thousands of startups are launched globally — but a significant number fail within the first few years due to:

- Poor revenue growth
- High burn rate with low cash runway
- Weak product-market fit
- Insufficient funding
- Inexperienced founding teams

Investors and founders currently rely on **manual analysis** to evaluate startup risk — a process that is slow, expensive, and highly subjective.

**Startup Risk Analyzer** solves this by providing an **automated, data-driven risk assessment** that instantly predicts a startup's probability of success or failure based on its key business metrics.

---

## 👥 Who is this for?

- **Investors** — Evaluate startup risk before making funding decisions
- **Founders** — Monitor your startup's health and identify weak areas
- **Incubators & VCs** — Assess portfolio risk at scale

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Data Processing | Python, Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Visualization | Matplotlib, Seaborn |
| Backend API | FastAPI, Uvicorn |
| Frontend Dashboard | Streamlit |
| Containerization | Docker |
| Version Control | Git, GitHub |

---

## 📊 Dataset

- **Source:** [Kaggle — Startup Funding and Outcome Dataset](https://www.kaggle.com/datasets/dhrubangtalukdar/startup-funding-and-outcome-dataset)
- **Size:** 1,00,000 rows × 11 columns
- **Target Variable:** `outcome` — Failure (0) or Success (1)

| Feature | Type | Description |
|---------|------|-------------|
| `funding_rounds` | Numeric | Number of funding rounds completed |
| `founder_experience_years` | Numeric | Years of founder experience |
| `team_size` | Numeric | Total team members |
| `market_size_billion` | Numeric | Target market size in billion USD |
| `product_traction_users` | Numeric | Number of active users |
| `burn_rate_million` | Numeric | Monthly cash burn in million USD |
| `revenue_million` | Numeric | Monthly revenue in million USD |
| `investor_type` | Categorical | Angel, Bootstrapped, Tier 1 VC, Tier 2 VC |
| `sector` | Categorical | AI, Climate, Crypto, Ecommerce, Fintech, Health, SaaS |
| `founder_background` | Categorical | Academic, Ex-BigTech, First-time, Serial Founder |
| `outcome` | Target | Failure / Acquisition / IPO |

---

## 🤖 ML Pipeline

### Feature Engineering
4 new features created to capture business health signals:

| Feature | Formula | Business Meaning |
|---------|---------|-----------------|
| `burn_efficiency` | revenue / burn_rate | How efficiently capital is being used |
| `revenue_per_employee` | revenue / team_size | Team productivity |
| `traction_per_employee` | users / team_size | Product growth per team member |
| `runway_risk` | burn_rate > revenue | 1 if cash runway is at risk |

### Model Comparison

| Model | Accuracy | ROC-AUC | CV ROC-AUC |
|-------|----------|---------|------------|
| **Logistic Regression** | **76.00%** | **0.8393** | **0.8391** |
| XGBoost | 75.44% | 0.8303 | 0.8294 |
| Random Forest | 75.25% | 0.8278 | 0.8266 |
| Decision Tree | 66.57% | 0.6619 | 0.6616 |

### Final Model — Logistic Regression

Logistic Regression was selected as the final model because:
- Highest accuracy and ROC-AUC across all evaluation metrics
- Most stable across 5-fold cross validation — std dev of only 0.0026
- `class_weight='balanced'` applied to improve recall for successful startups — reducing missed opportunities for investors
- Dataset contains strong linear patterns — Logistic Regression captures them effectively

### Key Findings from EDA
- Revenue and product traction are the strongest predictors of startup success
- Burn rate alone has negligible correlation with outcome — context matters
- Market size has almost zero correlation — execution matters more than opportunity size

---

## 📁 Project Structure

```bash
startup-risk-analyzer/
│
├── app/
│   ├── init.py
│   ├── main.py
│   └── predictor.py
│
├── dashboard/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
│
├── examples/
│   └── sample_request.json
│
├── models/
│   ├── final_pipeline.joblib
│   └── preprocessor.joblib
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_model_training.ipynb
│
├── tests/
│   ├── test_health.py
│   └── test_predict.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Option 1 — Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/md-faiyazkhan/startup-risk-analyzer.git
cd startup-risk-analyzer
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Download dataset**

Download the dataset from [Kaggle](https://www.kaggle.com/datasets/dhrubangtalukdar/startup-funding-and-outcome-dataset) and place it in `data/raw/`.

**4. Run notebooks in order**
01_eda.ipynb
02_preprocessing.ipynb
03_model_training.ipynb
This will generate `models/final_pipeline.joblib` automatically.

**5. Run Streamlit Dashboard**
```bash
streamlit run dashboard/streamlit_app.py
```

**6. Run FastAPI**
```bash
uvicorn app.main:app --reload
```

---

### Option 2 — Docker

**1. Build image**
```bash
docker build -t mdfaiyazkhan/startup-risk-analyzer .
```

**2. Run container**
```bash
docker run -p 8000:8000 -p 8501:8501 mdfaiyazkhan/startup-risk-analyzer
```

**3. Access**
- Streamlit: `http://localhost:8501`
- FastAPI Docs: `http://localhost:8000/docs`

## 🐳 Docker Hub

Image is publicly available on Docker Hub:

```bash
docker pull mdfaiyazkhan/startup-risk-analyzer
docker run -p 8000:8000 -p 8501:8501 mdfaiyazkhan/startup-risk-analyzer
```

---

## 📡 API Reference

**Endpoint:** `POST /predict`

**Sample Request:**
```json
{
    "funding_rounds": 3,
    "founder_experience_years": 5,
    "team_size": 20,
    "market_size_billion": 10.5,
    "product_traction_users": 5000,
    "burn_rate_million": 0.5,
    "revenue_million": 1.0,
    "investor_type": "tier1_vc",
    "sector": "Fintech",
    "founder_background": "ex_bigtech"
}
```

**Sample Response:**
```json
{
    "prediction": 1,
    "success_probability": 78.19,
    "failure_probability": 21.81,
    "risk_category": "Low Risk"
}
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🔮 Future Scope

- **Model Retraining Pipeline** — Automatically retrain model when new data arrives
- **Model Versioning** — Track experiments using MLflow
- **Database Integration** — Store predictions in MySQL for historical analysis
- **Batch Prediction** — Analyze multiple startups simultaneously
- **Model Monitoring** — Track model performance drift in production
- **Confidence Threshold** — Return "Inconclusive" when model confidence is low
- **Multi-industry Models** — Separate models optimized for different sectors

---

## ⚠️ Disclaimer

This tool is intended for informational purposes only. Predictions are based on historical startup data and should be used as a guide, not a definitive assessment. Always conduct thorough due diligence before making investment decisions.

---

## 👤 Author

**Md Faiyaz Khan**
- GitHub: [@md-faiyazkhan](https://github.com/md-faiyazkhan)
- LinkedIn: [@mdfaiyazkhan](www.linkedin.com/in/mdfaiyazkhan)
- Email: faiyazkhan.work@gmail.com
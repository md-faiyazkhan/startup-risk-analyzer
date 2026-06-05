import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load final pipeline
pipeline = joblib.load('../models/final_pipeline.joblib')

# Page configuration
st.set_page_config(
    page_title="Startup Risk Analyzer",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .risk-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .low-risk { background-color: #d4edda; color: #155724; }
    .medium-risk { background-color: #fff3cd; color: #856404; }
    .high-risk { background-color: #f8d7da; color: #721c24; }
    .metric-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 Startup Risk Analyzer")
st.markdown("Enter your startup details in the sidebar to get an instant risk assessment.")
st.divider()

# ── Sidebar ──────────────────────────────────────────────
st.sidebar.title("Startup Details")
st.sidebar.divider()

st.sidebar.subheader("📊 Business Metrics")
funding_rounds = st.sidebar.slider("Funding Rounds", min_value=0, max_value=8, value=2)
founder_experience_years = st.sidebar.slider("Founder Experience (Years)", min_value=0, max_value=24, value=5)
team_size = st.sidebar.number_input("Team Size", min_value=2, max_value=299, value=50, step=1)
market_size_billion = st.sidebar.number_input("Market Size (Billion USD)", min_value=0.0, value=10.0, step=0.5)
product_traction_users = st.sidebar.number_input("Product Traction (Users)", min_value=0, value=10000, step=1000)
burn_rate_million = st.sidebar.number_input("Burn Rate (Million USD/month)", min_value=0.0, value=1.0, step=0.1)
revenue_million = st.sidebar.number_input("Revenue (Million USD/month)", min_value=0.0, value=0.5, step=0.1)

st.sidebar.divider()

st.sidebar.subheader("🏢 Company Details")
investor_type = st.sidebar.selectbox("Investor Type",
                                      options=['angel', 'none', 'tier1_vc', 'tier2_vc'],
                                      format_func=lambda x: {
                                          'angel': 'Angel Investor',
                                          'none': 'Bootstrapped',
                                          'tier1_vc': 'Tier 1 VC',
                                          'tier2_vc': 'Tier 2 VC'
                                      }[x])

sector = st.sidebar.selectbox("Sector",
                               options=['AI', 'Climate', 'Crypto', 'Ecommerce', 'Fintech', 'Health', 'SaaS'])

founder_background = st.sidebar.selectbox("Founder Background",
                                           options=['academic', 'ex_bigtech', 'first_time', 'serial_founder'],
                                           format_func=lambda x: {
                                               'academic': 'Academic / Research',
                                               'ex_bigtech': 'Ex Big Tech',
                                               'first_time': 'First Time Founder',
                                               'serial_founder': 'Serial Founder'
                                           }[x])

st.sidebar.divider()
predict_button = st.sidebar.button("🔍 Analyze Risk", use_container_width=True)

# ── Main Area ─────────────────────────────────────────────
if not predict_button:
    st.markdown("### How it works")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 1. Enter Details")
        st.markdown("Fill in your startup's business metrics and company details in the sidebar.")

    with col2:
        st.markdown("#### 2. Analyze")
        st.markdown("Click **Analyze Risk** to run the prediction model.")

    with col3:
        st.markdown("#### 3. Get Results")
        st.markdown("Instantly see your startup's risk level and success probability.")

if predict_button:
    # ── Feature Engineering ───────────────────────────────
    burn_efficiency = revenue_million / burn_rate_million if burn_rate_million != 0 else 0
    revenue_per_employee = revenue_million / team_size if team_size != 0 else 0
    traction_per_employee = product_traction_users / team_size if team_size != 0 else 0
    runway_risk = 1 if burn_rate_million > revenue_million else 0

    # ── Input DataFrame ───────────────────────────────────
    input_data = pd.DataFrame({
        'funding_rounds': [funding_rounds],
        'founder_experience_years': [founder_experience_years],
        'team_size': [team_size],
        'market_size_billion': [market_size_billion],
        'product_traction_users': [product_traction_users],
        'burn_rate_million': [burn_rate_million],
        'revenue_million': [revenue_million],
        'investor_type': [investor_type],
        'sector': [sector],
        'founder_background': [founder_background],
        'burn_efficiency': [burn_efficiency],
        'revenue_per_employee': [revenue_per_employee],
        'traction_per_employee': [traction_per_employee],
        'runway_risk': [runway_risk]
    })

    # ── Prediction ────────────────────────────────────────
    prediction = pipeline.predict(input_data)[0]
    probability = pipeline.predict_proba(input_data)[0]
    failure_prob = round(probability[0] * 100, 2)
    success_prob = round(probability[1] * 100, 2)

    # ── Risk Category ─────────────────────────────────────
    if success_prob >= 75:
        risk_label = "Low Risk"
        risk_class = "low-risk"
        risk_emoji = "✅"
    elif success_prob >= 50:
        risk_label = "Medium Risk"
        risk_class = "medium-risk"
        risk_emoji = "⚠️"
    else:
        risk_label = "High Risk"
        risk_class = "high-risk"
        risk_emoji = "🚨"

    # ── Results Layout ────────────────────────────────────
    st.markdown("### Risk Assessment Results")
    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        # Risk Category Box
        st.markdown(f"""
            <div class="risk-box {risk_class}">
                <div style="font-size: 48px;">{risk_emoji}</div>
                <div style="font-size: 28px; font-weight: bold;">{risk_label}</div>
            </div>
        """, unsafe_allow_html=True)

        # Probabilities
        st.markdown("#### Success Probability")
        st.progress(int(success_prob))
        st.markdown(f"**{success_prob}%** chance of success")

        st.markdown("#### Failure Probability")
        st.progress(int(failure_prob))
        st.markdown(f"**{failure_prob}%** chance of failure")

    with col2:
        # Key Insights
        st.markdown("#### Key Insights")

        # Runway Risk
        if runway_risk == 1:
            st.error("Burn rate exceeds revenue — cash runway at risk")
        else:
            st.success("Revenue covers burn rate — healthy cash position")

        # Revenue
        if revenue_million >= 1.0:
            st.success("Strong revenue — good product market fit signal")
        elif revenue_million >= 0.5:
            st.warning("Moderate revenue — focus on growth")
        else:
            st.error("Low revenue — product market fit needs attention")

        # Funding
        if funding_rounds >= 3:
            st.success("Strong funding history — investor confidence high")
        elif funding_rounds >= 1:
            st.warning("Early stage funding — more rounds needed")
        else:
            st.error("No external funding — bootstrapped startup")

        # Founder Experience
        if founder_experience_years >= 10:
            st.success("Experienced founder — strong execution capability")
        elif founder_experience_years >= 5:
            st.warning("Moderate experience — good potential")
        else:
            st.error("Limited experience — higher execution risk")

    st.divider()
    st.caption("Note: This prediction is based on historical startup data and should be used as a guide, not a definitive assessment.")
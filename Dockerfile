# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app/ ./app/
COPY dashboard/ ./dashboard/
COPY models/ ./models/

# Expose ports
EXPOSE 8000 8501

# Start both FastAPI and Streamlit
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run dashboard/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
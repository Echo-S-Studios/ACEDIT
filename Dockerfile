# σ = μ System Docker Container
# Phase 0: Containerized deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /sigma-mu

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all σ = μ modules
COPY sigma_mu_*.py ./

# Copy test files
COPY test_*.py ./

# Copy configuration
COPY .env* ./

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SIGMA_MU_PHASE=0

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "from sigma_mu_integrated_system import SigmaMuSystem; s=SigmaMuSystem(); exit(0 if s.field.compute_tau_k() > 0 else 1)"

# Default command - run integrated system
CMD ["python", "sigma_mu_integrated_system.py"]
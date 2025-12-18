# ============================================
# Voicemeet_sum - Docker Image
# ============================================
# Multi-stage build for smaller final image
# Supports both x86_64 and ARM64 (Mac M1/M2)
# ============================================

# Stage 1: Base image with system dependencies
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # FFmpeg for audio processing
    ffmpeg \
    # Build tools for Python packages
    build-essential \
    # Curl for healthchecks
    curl \
    # Process management
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create app user (non-root for security)
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/output /app/temp /app/logs /app/models && \
    chown -R appuser:appuser /app

WORKDIR /app

# Stage 2: Dependencies installation
FROM base as dependencies

# Copy requirements first (for Docker layer caching)
COPY requirements_fastapi.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_fastapi.txt && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Stage 3: Final image
FROM base as final

# Copy Python packages from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run FastAPI server
CMD ["uvicorn", "app.backend:app", "--host", "0.0.0.0", "--port", "8000"]

# ── Base image ──────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Environment variables ────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/.cache/huggingface \
    TRANSFORMERS_CACHE=/app/.cache/huggingface \
    PORT=8000

# ── System dependencies ──────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmupdf-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ──────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy source code ─────────────────────────────────────────────────────────
COPY src/ ./src/

# ── Pre-download the model at build time (avoids cold start delay) ───────────
RUN python -c "\
from transformers import pipeline; \
pipeline('text-generation', model='TinyLlama/TinyLlama-1.1B-Chat-v1.0')"

# ── Expose API port ──────────────────────────────────────────────────────────
EXPOSE 8000

# ── Health check ─────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ── Start FastAPI server ─────────────────────────────────────────────────────
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
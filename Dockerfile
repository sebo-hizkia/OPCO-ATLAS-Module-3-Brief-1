# ───────── BASE IMAGE ─────────
FROM python:3.10-slim

# ───────── INSTALL SYSTEM DEPENDENCIES ─────────
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# ───────── SET WORKDIR ─────────
WORKDIR /app

# ───────── COPY REQUIREMENTS AND INSTALL ─────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ───────── COPY APPLICATION ─────────
COPY . .

# ───────── EXPOSE PORT ─────────
EXPOSE 9000

# ───────── LAUNCH API ─────────
CMD ["uvicorn", "app.predict_api:app", "--host", "0.0.0.0", "--port", "9000"]

FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy inference code
COPY inference /app/inference
COPY utils /app/utils
COPY traffic_metrics /app/traffic_metrics

ENV PYTHONPATH="/app"

CMD ["python", "-m", "inference.pipeline"]

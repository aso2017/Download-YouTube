FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.deno/bin:$PATH"

WORKDIR /app

# Install system dependencies:
# - ffmpeg: merge video/audio and convert media
# - unzip: required by Deno installer
# - curl/ca-certificates: download/install Deno
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        unzip \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deno.land/install.sh | sh \
    && deno --version

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application files
COPY . .

# Render health server / web service port
ENV PORT=10000
EXPOSE 10000

CMD ["python", "bot.py"]

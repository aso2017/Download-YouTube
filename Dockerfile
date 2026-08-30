FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DENO_INSTALL=/usr/local

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deno.land/install.sh | sh \
    && deno --version

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot.py .
COPY render.yaml .

RUN mkdir -p /tmp/downloads \
    && chmod 1777 /tmp/downloads

CMD ["python", "bot.py"]

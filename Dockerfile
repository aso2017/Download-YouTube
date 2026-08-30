FROM python:3.13-slim
WORKDIR /app
RUN apt update && apt install -y ffmpeg curl unzip && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deno.land/install.sh | sh
ENV PATH="/root/.deno/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python","bot.py"]

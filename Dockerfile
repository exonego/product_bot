# build
FROM python:3.12-slim-bullseye AS compile-image

WORKDIR /product_bot

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# run
FROM python:3.12-slim-bullseye AS run-image

WORKDIR /product_bot

COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
COPY . .

RUN chmod +x bin/entrypoint.sh
ENTRYPOINT ["./bin/entrypoint.sh"]

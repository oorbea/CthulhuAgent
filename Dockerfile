FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.in /app/requirements.in

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r /app/requirements.in


FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN useradd -m appuser && mkdir -p /app/documents && chown -R appuser:appuser /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY . /app
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--workers", "2"]

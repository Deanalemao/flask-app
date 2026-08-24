#stage 1
FROM python:3.11 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


#stage 2

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local

RUN useradd -m appuser

COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE 5000

CMD ["python","app.py"]


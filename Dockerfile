FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

RUN addgroup --system app && adduser --system --group app

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app/ ./app/

# Give ownership of the app directory to the app user
RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
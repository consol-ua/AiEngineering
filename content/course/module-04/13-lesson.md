## Урок 13. Containerization та 12-Factor App

### 13.1. Навіщо контейнеризувати AI-застосунок

Контейнер дозволяє упаковувати застосунок разом із необхідними залежностями та запускати його в узгодженому середовищі.

Але контейнер не гарантує повної відтворюваності сам по собі: важливо фіксувати версії залежностей, образів та конфігурацій.

### 13.2. Stateless Application

Для Cloud Run рекомендовано проєктувати основний API як stateless service.

Це означає, що критичний стан не повинен залежати від локальної файлової системи конкретного інстансу.

Зовнішні компоненти:

- Qdrant — векторний індекс.
- PostgreSQL — metadata та стан застосунку.
- Redis — кеш і rate limiting.
- Cloud Storage — документи.
- Secret Manager — секрети.

### 13.3. Dockerfile

```

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir \
    -r requirements.txt

COPY src/ ./src/

RUN useradd --create-home appuser
USER appuser

ENV PORT=8080

CMD ["sh", "-c", "exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]

```

Для production також варто використовувати dependency pinning, vulnerability scanning, `.dockerignore`, мінімальні базові образи та фіксацію image digest.


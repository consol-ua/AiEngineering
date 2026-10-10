# Тиждень 16. CI/CD, Google Cloud Run & Production Operations

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

## Урок 14. CI/CD Pipeline

### 14.1. Continuous Integration

CI перевіряє зміни до того, як вони потраплять у production.

Для AI-застосунку pipeline може включати:

`Lint → Unit Tests → Integration Tests → Security Checks → RAG Evaluation → Build`

### 14.2. Continuous Delivery

CD автоматизує підготовку та розгортання нових версій.

Для production корисно мати:

- Staging environment.
- Smoke tests.
- Quality gates.
- Manual approval для критичних змін.
- Rollback strategy.

### 14.3. GitHub Actions

```

name: AI Backend CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint
        run: ruff check .

      - name: Unit tests
        run: pytest tests/unit -q

      - name: Integration tests
        run: pytest tests/integration -q

```

Це базовий приклад. Інтеграційні тести повинні мати доступ до необхідних test services або mocks.

### 14.4. AI-specific Quality Gates

На відміну від звичайного backend, для AI-систем потрібно також перевіряти:

- Retrieval quality.
- Structured output validity.
- Prompt regressions.
- Tool routing.
- Groundedness.
- Cost budgets.

Не всі LLM evaluations варто запускати на кожен commit: частина може бути дорогою та нестабільною. Практичний підхід — швидкі deterministic tests у PR та ширші evaluations перед релізом.

## Урок 15. Deployment на Google Cloud Run

### 15.1. Чому Cloud Run

Cloud Run — керована платформа для запуску контейнеризованих застосунків.

Вона підходить для FastAPI та webhook-based сервісів, коли потрібно масштабувати HTTP workloads без керування власними серверами.

Для AI Knowledge Assistant Cloud Run може виконувати роль API та orchestration layer, тоді як Qdrant і stateful storage розміщуються окремо.

### 15.2. Production Architecture

### 15.3. Основні параметри Cloud Run

Concurrency: кількість одночасних запитів на інстанс.

Memory: доступна пам'ять.

CPU: обчислювальні ресурси.

Request timeout: максимальна тривалість HTTP-запиту.

Minimum instances: кількість інстансів, які залишаються доступними.

Maximum instances: обмеження масштабування.

Для AI API потрібно обирати ці параметри на основі навантажувального тестування, а не випадкових значень.

### 15.4. Deployment

Приклад:

```

gcloud run deploy ai-knowledge-assistant \
  --image REGION-docker.pkg.dev/PROJECT_ID/REPO/IMAGE:TAG \
  --region REGION \
  --service-account SERVICE_ACCOUNT_EMAIL \
  --memory 2Gi \
  --cpu 2 \
  --concurrency 10 \
  --timeout 300

```

Заміни placeholders на свої значення.

Ця команда припускає, що контейнерний образ уже створено й завантажено до Artifact Registry, а сервісний акаунт має необхідні дозволи.

Доступ до сервісу налаштовуй відповідно до сценарію. Не роби адміністративні endpoint-и публічними.

### 15.5. Secrets та IAM

Не передавай API keys через Docker image або GitHub repository.

Використовуй Secret Manager та service account із мінімально необхідними правами.

Для CI/CD краще використовувати короткоживучу федеративну автентифікацію, а не довгоживучі JSON service account keys.

## Урок 16. Production Readiness, Rollback & Incident Response

### 16.1. Production Readiness Checklist

Перед релізом перевір:

Reliability

- Є health endpoints.
- Налаштовані timeouts.
- Retries обмежені.
- Є fallback strategy.
- Фонові задачі не губляться.

Security

- Authentication та authorization працюють.
- Tenant isolation перевірено.
- Secrets зберігаються безпечно.
- Tool calls мають обмеження.
- Prompt injection scenarios протестовано.

Observability

- Є logs, metrics, traces.
- Відстежуються latency і витрати.
- Налаштовані alerts.
- Можна діагностувати невдалий запит.

Deployment

- Є staging.
- CI/CD проходить.
- Є smoke tests.
- Підготовлено rollback.
- Є backup strategy.

### 16.2. Rollback

Rollback — повернення до попередньої стабільної версії.

Для AI-систем важливо враховувати, що код, промпти, embedding-модель та vector index можуть мати різні версії.

Наприклад, rollback застосунку не допоможе, якщо нова версія вже змінила формат embeddings у спільній колекції.

Тому варто використовувати versioned indexes або окремі колекції з контрольованим перемиканням.

### 16.3. Incident Response

Для production AI потрібно мати план дій у разі:

- Недоступності LLM-провайдера.
- Зростання latency.
- Перевищення витрат.
- Витоку даних.
- Неправильних tool calls.
- Падіння якості відповідей.
- Пошкодження індексу.

Для кожного інциденту визначай спосіб виявлення, відповідальних осіб, процедуру обмеження впливу та відновлення.

### Лабораторна робота №16

Розгорни AI Knowledge Assistant на Cloud Run.

Необхідно:

1. Створити Docker image.
2. Налаштувати Artifact Registry.
3. Налаштувати Secret Manager.
4. Підключити зовнішній Qdrant.
5. Створити CI/CD pipeline.
6. Розгорнути staging environment.
7. Виконати smoke tests.
8. Перевірити rollback.
9. Налаштувати monitoring та alerts.
10. Підготувати README й deployment runbook.

Критерії завершення: сервіс доступний у staging, проходить smoke tests, використовує зовнішнє сховище стану, має контрольований доступ та задокументовану процедуру відновлення.

### Матеріали тижня 16

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- [GitHub Actions](https://docs.github.com/en/actions)
- [The Twelve-Factor App](https://12factor.net/)


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


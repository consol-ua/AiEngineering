# Фінальний проєкт усього курсу

## AI Knowledge Assistant — Production Edition

Тепер потрібно об'єднати результати всіх чотирьох модулів.

### Повна архітектура

## Функціональні вимоги

Готовий застосунок повинен:

- Завантажувати PDF, DOCX та HTML.
- Індексувати документи в Qdrant.
- Виконувати hybrid search із reranking.
- Генерувати відповіді з цитуванням джерел.
- Підтримувати agentic tool calling.
- Використовувати власний MCP Server.
- Зберігати стан розмови.
- Працювати через FastAPI.
- Підтримувати streaming.
- Мати authentication та tenant isolation.
- Записувати traces і usage metrics.
- Виконувати автоматизовані evaluations.
- Розгортатися через CI/CD на Cloud Run.

## Definition of Done

Готовність фінального проєкту

Перевірте всі 18 критеріїв готовності:

- FastAPI API працює асинхронно
- Реалізовано authentication та authorization
- Tenant isolation перевірено
- Працює SSE streaming
- Реалізовано rate limiting
- Timeouts і retries обмежені
- Є idempotency для write-операцій
- Проведено performance benchmark
- Вимірюється cost per successful task
- Реалізовано model routing
- Проведено security testing
- Додано structured logging і tracing
- Secrets не зберігаються в репозиторії
- Є CI/CD із тестами
- Сервіс розгорнуто на Cloud Run
- Виконано staging smoke tests
- Підготовлено rollback procedure
- Є deployment runbook



## Що ти знатимеш після завершення курсу

За 16 тижнів ти пройдеш шлях від базових принципів LLM до розробки й підтримки AI-системи, яка використовує власні дані, інструменти, агентну оркестрацію та production infrastructure.

Важливо, що результатом буде не просто демонстраційний чатбот, а повноцінний AI Engineering portfolio project, який можна показувати на технічних співбесідах, використовувати як основу власного продукту або розвивати далі.

Наступним логічним кроком стане поглиблення матеріалів: архітектурні кейси, production-приклади коду, повні лабораторні роботи з тестами, питання для самоперевірки та окремі завдання для підготовки до AI Engineer interview.

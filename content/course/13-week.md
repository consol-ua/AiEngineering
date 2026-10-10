# Тиждень 13. Production API Architecture & Reliability

## Урок 1. Архітектура production AI-застосунку

### 1.1. Чим AI Backend відрізняється від звичайного Backend

Звичайний backend часто працює з передбачуваними операціями: читанням даних, валідацією, записом у базу, обчисленнями.

AI Backend додає декілька особливостей:

- Виклики LLM можуть тривати десятки секунд.
- Latency залежить від довжини контексту та відповіді.
- Відповіді моделей можуть бути невалідними.
- Провайдер може обмежувати кількість запитів і токенів.
- Один користувацький запит може запускати кілька LLM-викликів.
- Вартість операції залежить від фактичного використання.
- Інструменти агента можуть мати побічні ефекти.

Тому важливо розділити API, orchestration, AI inference, retrieval та infrastructure.

### 1.2. Рекомендована архітектура

### 1.3. Modular Monolith vs Microservices

Для першого production AI-застосунку зазвичай краще почати з modular monolith.

Це один застосунок із чітко розділеними модулями:

```
api/
auth/
orchestration/
retrieval/
llm/
tools/
observability/
```

Переваги:

- Простіший deployment.
- Менше мережевих викликів.
- Легше налагодження.
- Простіше локальне тестування.
- Менші операційні витрати.

Microservices доцільні, коли окремі компоненти мають незалежні вимоги до масштабування, ізоляції чи життєвого циклу.

Best practice: не розділяй систему на мікросервіси лише тому, що в ній використовуються AI Agents.

## Урок 2. Async Processing, Background Jobs & Streaming

### 2.1. Async I/O

У FastAPI асинхронність корисна для операцій, які очікують відповіді від зовнішніх сервісів:

- LLM API.
- Qdrant.
- Redis.
- HTTP-інструменти.
- Бази даних з async-драйверами.

Але `async def` не робить CPU-bound операції автоматично неблокувальними.

Наприклад, локальна embedding-модель може виконувати важкі обчислення й блокувати event loop, якщо її викликати безпосередньо.

Для таких задач можуть знадобитися worker pool, окремі процеси або спеціалізований inference-сервіс.

### 2.2. BackgroundTasks vs Queue

FastAPI `BackgroundTasks` підходить для простих некритичних задач після HTTP-відповіді.

Але для тривалого ingestion великих PDF, embeddings або масової індексації краще використовувати надійну чергу.

| Характеристика               | BackgroundTasks      | Durable Queue              |
| ---------------------------- | -------------------- | -------------------------- |
| Простота                     | Висока               | Нижча                      |
| Переживає завершення процесу | Не гарантується      | За правильної конфігурації |
| Retries                      | Потрібно реалізувати | Часто підтримуються        |
| Масштабування workers        | Обмежене             | Гнучкіше                   |
| Великі ingestion jobs        | Небажано             | Рекомендовано              |

Для Google Cloud можна розглядати Cloud Tasks або Pub/Sub залежно від вимог.

### 2.3. Server-Sent Events

SSE дозволяє передавати події від сервера до клієнта через HTTP.

Приклад із FastAPI:

```python
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def generate_tokens():
    for token in ["Привіт", ", ", "світе!"]:
        payload = json.dumps({"token": token}, ensure_ascii=False)
        yield f"event: token\ndata: {payload}\n\n"
    yield "event: done\ndata: {}\n\n"

@app.get("/stream")
async def stream():
    return StreamingResponse(
        generate_tokens(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
```

Це демонстрація SSE-протоколу, а не реальний LLM streaming.

У production потрібно враховувати cancellation, client disconnect, backpressure, proxy buffering і завершення потоку з помилкою.

### Best Practices

- Не виконуй важкий CPU inference в event loop.
- Використовуй durable queue для критичних фонових задач.
- Не передавай секрети в SSE-подіях.
- Обмежуй кількість одночасних LLM-викликів.
- Коректно обробляй відключення клієнта.
- Передбачай окрему подію помилки в streaming-протоколі.

## Урок 3. Timeouts, Retries, Circuit Breakers & Bulkheads

### 3.1. Чому retries недостатньо

Припустимо, один запит до агента запускає три зовнішні інструменти.

Якщо кожен інструмент має по три retries, кількість фактичних викликів може швидко зрости.

Це збільшує latency, витрати й навантаження на нестабільні сервіси.

Тому потрібно керувати загальним бюджетом виконання, а не лише retries окремих HTTP-клієнтів.

### 3.2. Timeout Hierarchy

Приклад:

```
User request deadline: 30 seconds
  |
  +-- Retrieval: 3 seconds
  +-- Reranking: 4 seconds
  +-- LLM generation: 20 seconds
  +-- Response processing: 3 seconds
```

Це умовні значення. У реальній системі бюджети визначаються на основі latency requirements та вимірювань.

### 3.3. Circuit Breaker

Circuit breaker запобігає безконтрольним викликам нестабільного сервісу.

Стани:

- Closed: запити виконуються.
- Open: запити тимчасово блокуються.
- Half-open: обмежена кількість запитів перевіряє відновлення.

### 3.4. Bulkhead Pattern

Bulkhead ізолює ресурси різних категорій операцій.

Наприклад, ingestion не повинен споживати всі доступні з'єднання й блокувати відповіді користувачам.

Практичні механізми:

- Окремі concurrency limits.
- Окремі worker pools.
- Окремі черги.
- Resource quotas.

### 3.5. Idempotency

Якщо агент виконує write-операцію, retry може створити дублікати.

Наприклад, повторний `create_ticket` може створити два однакові звернення.

Для таких операцій використовуй idempotency keys, транзакційні гарантії або механізми дедуплікації.

Best practices

- Не повторюй неідемпотентні операції без захисту.
- Використовуй exponential backoff із jitter.
- Обмежуй retry budget.
- Розрізняй transient і permanent errors.
- Встановлюй end-to-end deadline.
- Не використовуй fallback, який порушує вимоги безпеки або якості.

## Урок 4. Authentication, Authorization & Rate Limiting

### 4.1. Authentication vs Authorization

Authentication відповідає на питання: хто виконує запит?

Authorization відповідає на питання: чи має цей користувач право виконати операцію?

У RAG це особливо важливо, тому що один індекс може містити документи різних користувачів або організацій.

### 4.2. Tenant Isolation

Припустимо, у Qdrant зберігаються документи компаній A та B.

Користувач компанії A не повинен отримати фрагменти документів компанії B, навіть якщо вони дуже релевантні його запиту.

Тому tenant filtering потрібно застосовувати до формування контексту для LLM.

```python
from qdrant_client import models

# authenticated_tenant_id надходить із перевіреного серверного контексту.
tenant_filter = models.Filter(must=[
    models.FieldCondition(
        key="tenant_id",
        match=models.MatchValue(value=authenticated_tenant_id),
    )
])
```

`authenticated_tenant_id` повинен надходити з перевіреного серверного контексту автентифікації, а не з довільного поля користувацького запиту.

### 4.3. Rate Limiting

Rate limiting захищає систему від перевантаження та неконтрольованих витрат.

Можливі обмеження:

- Requests per minute.
- Tokens per minute.
- Concurrent requests.
- Daily budget per user.
- Monthly budget per tenant.

### Лабораторна робота №13

Підготуй production API для AI Knowledge Assistant.

Реалізуй:

1. Authentication middleware.
2. Tenant isolation.
3. Rate limiting через Redis.
4. Async LLM requests.
5. SSE streaming.
6. Request timeout.
7. Retry policy.
8. Idempotency для write-операцій.
9. Health endpoints.

Критерії завершення: користувачі ізольовані; перевищення лімітів обробляється; зовнішні збої не спричиняють нескінченних retries; streaming завершується коректно.

### Матеріали тижня 13

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/docs/latest/)
- [Google Cloud Tasks](https://cloud.google.com/tasks/docs)
- [Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/)


## Урок 15. Agent Reliability & Observability

### 15.1. Основні режими відмов

Агентна система може зазнавати збоїв на різних рівнях:

Model failure: неправильне рішення моделі.

Tool failure: зовнішній сервіс недоступний.

State failure: втрачений або пошкоджений стан.

Orchestration failure: неправильний перехід між вузлами.

Security failure: неавторизований доступ або виконання забороненої дії.

### 15.2. Retry Policy

Не всі помилки потрібно повторювати.

| Ситуація              | Рекомендована реакція              |
| --------------------- | ---------------------------------- |
| Network timeout       | Обмежений retry                    |
| Rate limit            | Backoff                            |
| Invalid arguments     | Валідація та корекція              |
| Permission denied     | Завершити без retry                |
| Tool unavailable      | Fallback або контрольована помилка |
| Maximum steps reached | Зупинити виконання                 |

### 15.3. Idempotency

Якщо агент створює зовнішній ресурс, повторний виклик може створити дубль.

Наприклад, після network timeout невідомо, чи GitHub issue було створено.

Тому для операцій зі зміною стану потрібні idempotency keys або перевірка фактичного результату перед повтором.

### 15.4. Observability

Для кожного виконання агента корисно записувати:

```
trace_id
thread_id
user_id
model
prompt_version
tool_name
tool_latency_ms
step_number
total_tokens
estimated_cost
execution_status
error_type
```

Не варто записувати персональні дані, секрети або повні tool results без потреби.

### 15.5. Distributed Tracing

OpenTelemetry та спеціалізовані AI-observability інструменти дозволяють пов'язати всі кроки виконання одним trace.

Наприклад:

```
POST /ask
  ├── agent_router
  ├── search_documents
  │   └── qdrant.query
  ├── reranker
  ├── llm.generate
  └── response_validation
```

Це допомагає знаходити причини високої latency та помилок.


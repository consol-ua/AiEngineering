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


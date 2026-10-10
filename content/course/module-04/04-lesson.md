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

# Тиждень 14. LLM Performance, Cost Optimization & Model Routing


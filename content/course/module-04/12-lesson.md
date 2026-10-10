## Урок 12. Observability для AI Pipelines

### 12.1. Monitoring vs Observability vs Evaluation

Monitoring відповідає на питання: чи працює система в межах очікуваних показників?

Observability допомагає зрозуміти, чому система поводиться певним чином.

Evaluation визначає, наскільки якісно система виконує поставлену задачу.

Ці поняття пов'язані, але не взаємозамінні.

### 12.2. Logs, Metrics, Traces

Logs — окремі події виконання.

Metrics — числові показники в часі.

Traces — послідовності пов'язаних операцій одного запиту.

Для RAG trace може виглядати так:

```
request_id=abc123
  |
  +-- authentication: 12 ms
  +-- query_embedding: 45 ms
  +-- vector_search: 31 ms
  +-- reranking: 120 ms
  +-- llm_generation: 1450 ms
  +-- validation: 8 ms
```

Значення умовні.

### 12.3. Langfuse

Langfuse — платформа для LLM observability та evaluations.

Вона дозволяє аналізувати LLM-виклики, traces, prompts, usage та інші аспекти AI-застосунків.

### 12.4. Метрики production AI

| Категорія   | Метрики                                |
| ----------- | -------------------------------------- |
| Reliability | Error rate, timeout rate, availability |
| Performance | p50/p95 latency, TTFT                  |
| Cost        | Tokens, estimated cost, cost per task  |
| RAG         | Recall@K, groundedness, abstention    |
| Agents      | Tool success rate, steps per task      |
| Security    | Denied tool calls, access violations   |
| Product     | Task completion rate, user feedback    |

### 12.5. Alerts

Приклади умов для сповіщень:

- Різке зростання 5xx.
- Збільшення p95 latency.
- Перевищення cost budget.
- Аномальне зростання tool calls.
- Падіння частки успішних задач.
- Підвищення частоти відмов у доступі.

### Лабораторна робота №15

Створи security та observability layer.

Потрібно:

1. Додати structured logging.
2. Інтегрувати Langfuse або OpenTelemetry.
3. Записувати traces для RAG та агентних викликів.
4. Реалізувати redaction чутливих полів.
5. Додати audit logs для write-інструментів.
6. Підготувати 20 adversarial test cases.
7. Перевірити prompt injection, tenant isolation і небезпечні tool calls.

Критерії завершення: можна відстежити повний життєвий цикл запиту; секрети не потрапляють у logs; неавторизовані операції блокуються; результати security tests задокументовані.

### Матеріали тижня 15

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [Langfuse Documentation](https://langfuse.com/docs)
- [OpenTelemetry](https://opentelemetry.io/docs/)
- [Google Secret Manager](https://cloud.google.com/secret-manager/docs)

# Тиждень 16. CI/CD, Google Cloud Run & Production Operations


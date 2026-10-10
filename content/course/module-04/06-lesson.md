## Урок 6. LLM Cost Engineering

### 6.1. З чого складається вартість AI-запиту

Для hosted LLM API:

```formula
C_LLM = (TᵢPᵢ + TₒPₒ) / 10⁶
```

де:

- T_i — input tokens.
- T_o — output tokens.
- P_i — ціна мільйона input tokens.
- P_o — ціна мільйона output tokens.

Але для RAG-системи повна вартість включає більше компонентів:

```formula
C_total = C_LLM + C_embeddings + C_retrieval + C_infrastructure + C_operations
```

Для agentic workflow потрібно враховувати всі виклики моделі та інструментів.

### 6.2. Cost per Successful Task

Це одна з найкорисніших метрик для AI-продукту.

```formula
C_successful_task = C_all_attempts / N_successful_tasks
```

Наприклад, одна модель може бути дешевшою за виклик, але вимагати більше повторів і частіше помилятися.

Тому вибір моделі лише за ціною токенів — антипатерн.

### 6.3. Token Budgeting

Для кожного сценарію визначай:

- Максимальний input context.
- Максимальний output.
- Кількість retrieval chunks.
- Максимальну кількість agent steps.
- Кількість retries.
- Максимальну вартість одного запиту.

### Best Practices

- Вимірюй фактичні витрати, а не лише теоретичні.
- Зберігай usage metadata.
- Використовуй budget alerts.
- Встановлюй per-user і per-tenant limits.
- Оцінюй якість разом із вартістю.
- Не оптимізуй токени ціною суттєвого погіршення результату.


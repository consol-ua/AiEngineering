## Урок 12. Tokenomics та Observability

### 12.1. Вартість LLM-запиту

Якщо API тарифікується за кількістю токенів, приблизну вартість можна обчислити так:

```formula
C = (TᵢPᵢ + TₒPₒ) / 10⁶
```

де Tᵢ, Tₒ — кількість токенів, а Pᵢ, Pₒ — ціна за мільйон токенів.

### 12.2. Метрики LLM Gateway

Мінімально записуй:

```
request_id
provider
model
prompt_version
latency_ms
input_tokens
output_tokens
estimated_cost
status
error_type
```

У production не варто без потреби зберігати повні промпти, відповіді або персональні дані.

### 12.3. Cost per Successful Task

Важлива не лише ціна запиту, а й те, скільки коштує досягнення потрібного результату.

Наприклад, модель A може коштувати дешевше за один виклик, але частіше генерувати невалідний JSON. Якщо потрібно багато повторів, її фактична економічність може бути гіршою.

### Лабораторна робота №3

Реалізуй LLM Gateway із такими функціями:

- Підтримка Ollama та одного хмарного провайдера.
- Єдиний Python-інтерфейс.
- Async requests.
- Streaming.
- Timeout і retry.
- Облік токенів, якщо usage доступний.
- Latency metrics.
- Mock provider для тестів.

Критерії завершення: однакові тестові сценарії працюють через обидва провайдери; збої обробляються; streaming коректно завершується; unit tests не потребують реального API.

Матеріали: [OpenAI Python SDK](https://github.com/openai/openai-python), [Ollama API](https://docs.ollama.com/api/), [Latency Optimization](https://platform.openai.com/docs/guides/latency-optimization).

# Тиждень 4. Prompt Engineering та Structured Outputs


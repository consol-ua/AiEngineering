# Тиждень 3. LLM API Engineering

## Урок 9. Архітектура LLM Gateway

LLM Gateway — це програмний шар, який відокремлює бізнес-логіку від конкретного inference-провайдера.

Він відповідає за маршрутизацію запитів, нормалізацію результатів, обробку помилок, метрики та контроль використання моделей.

### 9.1. Навіщо потрібна абстракція

Без Gateway бізнес-логіка залежатиме від SDK конкретного провайдера.

Це ускладнює:

- Перемикання моделей.
- A/B-тестування.
- Fallback.
- Порівняння вартості.
- Тестування без реальних API-викликів.

Однак не потрібно створювати надмірно складну абстракцію. Достатньо визначити операції, які реально потрібні застосунку.

### 9.2. Контракт LLM Provider

```python
from typing import Protocol
from pydantic import BaseModel

class LLMResponse(BaseModel):
    text: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None

class LLMProvider(Protocol):
    async def generate(self, messages: list[dict[str, str]]) -> LLMResponse:
        ...
```

Це базовий контракт. Для production можуть знадобитися окремі типи для tool calls, streaming events, usage metadata та structured outputs.

Best practice: не намагайся приховати всі відмінності моделей за однією універсальною функцією. Частина можливостей провайдерів принципово відрізняється.

## Урок 10. Reliability, Timeouts, Retries та Rate Limits

### 10.1. Класифікація помилок

| Помилка          | Типова реакція                            |
| ---------------- | ----------------------------------------- |
| HTTP 400         | Перевірити запит, не повторювати без змін |
| HTTP 401/403     | Перевірити авторизацію                    |
| HTTP 429         | Retry за політикою rate limiting          |
| HTTP 5xx         | Обмежені повторні спроби                  |
| Network timeout  | Retry, якщо операція безпечна             |
| Invalid output   | Валідація, можлива корекція               |
| Context overflow | Скоротити контекст                        |

### 10.2. Exponential Backoff

Поширена формула:

```formula
delayₙ = min(d_max, d₀ × 2ⁿ) + jitter
```

Jitter додає випадкову затримку, щоб багато клієнтів не повторювали запити одночасно.

### 10.3. Circuit Breaker

Circuit breaker тимчасово припиняє виклики до нестабільного сервісу після певної кількості збоїв.

Типові стани:

- Closed — запити дозволені.
- Open — виклики тимчасово блокуються.
- Half-open — обмежена перевірка відновлення сервісу.

Для невеликого навчального проєкту circuit breaker можна залишити додатковою вправою. Для систем із високим навантаженням він може бути корисним.

### Best Practices

- Встановлюй timeout на рівні одного виклику й загальний deadline операції.
- Обмежуй кількість retries.
- Поважай `Retry-After`, коли він надається.
- Не повторюй безконтрольно операції з побічними ефектами.
- Відокремлюй provider errors від validation errors.
- Не приховуй усі помилки за загальним `except Exception`.

## Урок 11. Streaming та Async Inference

### 11.1. Навіщо потрібен streaming

Streaming дозволяє повертати частини відповіді під час генерації.

Це покращує сприйняття швидкості, особливо для довгих відповідей.

Однак потрібно враховувати, що після початку streaming HTTP status уже не завжди можна змінити на звичайну помилку. Тому протокол має передбачати спеціальні події завершення та помилок.

### 11.2. Streaming із Python SDK

```python
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def stream_answer(prompt: str):
    stream = await client.chat.completions.create(
        model="YOUR_MODEL_ID",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
```

Це базовий приклад. У production додай cancellation, фінальні usage metrics, обробку винятків та контроль доступу.

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


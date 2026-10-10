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


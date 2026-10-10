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


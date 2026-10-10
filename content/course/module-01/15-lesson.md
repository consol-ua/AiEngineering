## Урок 15. Structured Outputs, JSON Schema та Pydantic

### 15.1. Чому звичайного JSON недостатньо

LLM може повернути синтаксично коректний JSON, який не відповідає бізнес-вимогам.

Наприклад:

```
{
  "category": "unknown_category",
  "confidence": 150
}
```

JSON валідний, але значення не відповідають очікуваному контракту.

### 15.2. Валідація через Pydantic

```python
from enum import Enum
from pydantic import BaseModel, Field

class Category(str, Enum):
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    LEGAL = "legal"
    OTHER = "other"

class ClassificationResult(BaseModel):
    category: Category
    confidence: float = Field(ge=0, le=1)
    summary: str = Field(min_length=1)
```

### 15.3. Schema-constrained Generation

Деякі API дозволяють передати JSON Schema або Pydantic-модель безпосередньо до механізму structured outputs.

Це може значно підвищити надійність формату, але не гарантує фактичної правильності полів.

Наприклад, `confidence=0.95` є валідним числом, але це не означає, що модель правильно відкалібрована і справді має 95% імовірності бути правильною.

Best practices

- Використовуй native structured outputs, коли вони підтримуються.
- Перевіряй відповідь через Pydantic.
- Окремо перевіряй бізнес-правила.
- Передбачай випадки refusal та incomplete output.
- Не припускай, що всі провайдери однаково підтримують JSON Schema.
- Не довіряй згенерованому confidence без калібрування.


## Урок 16. Prompt Evaluation та Versioning

### 16.1. Чому потрібні тести промптів

Промпт може добре працювати на п'яти прикладах, але погано — на реальних користувацьких запитах.

Тому створюй evaluation dataset із різними категоріями випадків:

- Типові вхідні дані.
- Порожні або неповні дані.
- Неоднозначні документи.
- Дуже довгі документи.
- Некоректне форматування.
- Спроби prompt injection.

### 16.2. Версіонування

Рекомендована структура:

```

prompts/
├── classification/
│   ├── v1.yaml
│   ├── v2.yaml
│   └── test_cases.json
└── extraction/
    ├── v1.yaml
    └── test_cases.json

```

Для кожного тестового запуску зберігай версію промпту, модель, параметри, результат і метрики.

### 16.3. Метрики

Для класифікації:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Invalid output rate.

Для extraction:

- Field-level accuracy.
- Schema validation success rate.
- Missing field rate.
- Hallucinated field rate.

### Лабораторна робота №4

Створи сервіс класифікації документів.

Він повинен:

1. Приймати текст.
2. Визначати категорію.
3. Повертати structured output.
4. Перевіряти відповідь через Pydantic.
5. Обробляти помилки.
6. Записувати метрики.
7. Порівнювати дві версії промпту.

Критерії завершення: щонайменше 30 тестових документів, не менше 90% schema-valid outputs, окремий звіт про точність класифікації та перевірка негативних сценаріїв.

Матеріали: [Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/), [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs), [Pydantic](https://docs.pydantic.dev/latest/).


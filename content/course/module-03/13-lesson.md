## Урок 13. AI-assisted Software Development

### 13.1. Роль AI у процесі розробки

AI-інструменти можуть допомагати з:

- Генерацією boilerplate-коду.
- Аналізом помилок.
- Написанням тестів.
- Рефакторингом.
- Поясненням складного коду.
- Створенням документації.
- Аналізом pull requests.
- Підготовкою міграцій.

Але згенерований код не варто автоматично вважати правильним або безпечним.

### 13.2. AI Development Workflow

Рекомендована схема:

`Requirements → Design → Implementation → Tests → Review → Integration`

Requirements: визначаємо очікувану поведінку.

Design: описуємо архітектуру та обмеження.

Implementation: створюємо невеликий, перевірюваний фрагмент.

Tests: перевіряємо функціональність.

Review: аналізуємо безпеку, складність і підтримуваність.

Integration: інтегруємо лише перевірені зміни.

### 13.3. Specification-driven Development

Замість запиту:

> Напиши AI-агента.

Краще надати специфікацію:

```
Task:
Implement a document search tool.

Technology:
Python 3.12, FastAPI, Pydantic v2, Qdrant.

Requirements:
- Async interface
- Tenant filtering
- Maximum 10 results
- Timeout handling
- Structured response
- Unit tests

Constraints:
- No global mutable state
- No hardcoded secrets
- No unvalidated user input
```

Чим чіткіший контракт, тим простіше перевіряти результат.

### 13.4. AI Coding Best Practices

- Працюй невеликими змінами.
- Проси пояснювати архітектурні компроміси.
- Перевіряй актуальність бібліотек і API.
- Не приймай код без тестів.
- Не передавай секрети в промпти.
- Використовуй Ruff, mypy, pytest та інші перевірки.
- Аналізуй зміни перед merge.
- Не дозволяй AI безконтрольно виконувати destructive commands.


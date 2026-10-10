## Урок 14. CI/CD Pipeline

### 14.1. Continuous Integration

CI перевіряє зміни до того, як вони потраплять у production.

Для AI-застосунку pipeline може включати:

`Lint → Unit Tests → Integration Tests → Security Checks → RAG Evaluation → Build`

### 14.2. Continuous Delivery

CD автоматизує підготовку та розгортання нових версій.

Для production корисно мати:

- Staging environment.
- Smoke tests.
- Quality gates.
- Manual approval для критичних змін.
- Rollback strategy.

### 14.3. GitHub Actions

```

name: AI Backend CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint
        run: ruff check .

      - name: Unit tests
        run: pytest tests/unit -q

      - name: Integration tests
        run: pytest tests/integration -q

```

Це базовий приклад. Інтеграційні тести повинні мати доступ до необхідних test services або mocks.

### 14.4. AI-specific Quality Gates

На відміну від звичайного backend, для AI-систем потрібно також перевіряти:

- Retrieval quality.
- Structured output validity.
- Prompt regressions.
- Tool routing.
- Groundedness.
- Cost budgets.

Не всі LLM evaluations варто запускати на кожен commit: частина може бути дорогою та нестабільною. Практичний підхід — швидкі deterministic tests у PR та ширші evaluations перед релізом.


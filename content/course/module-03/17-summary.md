# Підсумковий проєкт модуля 3

## Agentic Knowledge Assistant

Потрібно розширити Document RAG Assistant із модуля 2 до повноцінного агентного застосунку.

### Архітектура

### Функціональні вимоги

Система повинна підтримувати:

1. Діалог через FastAPI.
2. Пошук у документах через RAG.
3. Виклик інструментів через MCP.
4. Керування workflow через LangGraph.
5. Збереження історії розмов.
6. Context budgeting.
7. Контроль кількості кроків.
8. Авторизацію інструментів.
9. Human approval для критичних дій.
10. Автоматизоване оцінювання.

### Рекомендована структура проєкту

```

agentic-knowledge-assistant/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   └── approvals.py
│   │   └── dependencies.py
│   ├── agents/
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── routing.py
│   ├── tools/
│   │   ├── search.py
│   │   ├── calculator.py
│   │   └── registry.py
│   ├── mcp_server/
│   │   └── server.py
│   ├── memory/
│   │   ├── checkpoint.py
│   │   ├── summary.py
│   │   └── store.py
│   ├── context/
│   │   ├── builder.py
│   │   └── budget.py
│   ├── security/
│   │   ├── policies.py
│   │   └── approvals.py
│   └── observability/
│       └── tracing.py
├── evals/
│   ├── dataset.json
│   ├── metrics.py
│   └── runner.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── security/
├── pyproject.toml
└── docker-compose.yml

```

## Definition of Done

Готовність до модуля 4

Перевірте всі 15 критеріїв завершення.

- Розумію різницю між workflow, agent і multi-agent
- Реалізував function/tool calling із валідацією
- Створив LangGraph workflow із conditional routing
- Реалізував власний MCP Server
- Підключив MCP Client та tool discovery
- Додав short-term memory
- Реалізував checkpointing і відновлення стану
- Додав context budgeting
- Підключив Agentic RAG
- Обмежив agent loops та retries
- Реалізував authorization і tenant isolation
- Додав human approval для критичних дій
- Створив evaluation dataset із 50 сценаріїв
- Вимірюю task success, latency та tool accuracy
- Додав tracing і regression testing

## Підсумок модуля

Після завершення тижнів 9–12 ти повинен уміти проєктувати AI-агентів, підключати інструменти через MCP, керувати багатокроковим виконанням через LangGraph, реалізовувати пам'ять і context engineering та перевіряти надійність агентної системи.

Головний принцип: агентність має бути контрольованою, вимірюваною та обґрунтованою потребами задачі. Складніша архітектура не завжди означає кращу систему.

Наступний модуль — тижні 13–16: Production AI Engineering, LLMOps, Deployment & Monitoring. У ньому розглянемо Docker, Google Cloud Run, CI/CD, production observability, оптимізацію latency та витрат, безпеку розгортання і фінальний capstone-проєкт.

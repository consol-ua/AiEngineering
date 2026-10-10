# Підсумок курсу

# Підсумковий проєкт модуля 1

## LLM Gateway + Document Classification

Об'єднай усі чотири тижні в один застосунок.

Мінімальна архітектура:

```
FastAPI
  |
  +-- POST /generate
  +-- POST /classify
  +-- POST /generate/stream
  |
LLM Gateway
  |
  +-- Ollama Provider
  +-- Cloud Provider
  |
Validation
  |
  +-- Pydantic
  +-- Prompt Versions
  +-- Metrics
```

## Definition of Done

Готовність до наступного модуля: перевірте всі 12 критеріїв.

- Розумію Transformer, attention, tokenization та inference
- Можу пояснити temperature, top-p, KV cache і context window
- Запустив і порівняв дві локальні LLM
- Реалізував LLMProvider abstraction
- Підключив Ollama та хмарний API
- Додав async requests, timeouts і retry
- Реалізував streaming
- Відстежую latency та використання токенів
- Створив версіоновані промпти
- Використовую Pydantic та structured outputs
- Маю щонайменше 30 evaluation cases
- Усі unit tests проходять без реальних API-запитів

## Як поглиблювати матеріал

Для системного навчання використовуй такий порядок: спочатку прочитай теорію уроку, потім переглянь рекомендоване відео або документацію, відтвори приклад коду, зміни його параметри й нарешті виконай лабораторну роботу без копіювання готового рішення.

Окремо веди `learning-notes.md`, де записуй не тільки визначення, а й результати експериментів, помилки та архітектурні рішення.

Після модуля 1 ти матимеш фундамент для наступного етапу — Data Ingestion, Embeddings, Vector Databases та RAG. Саме там навчимо LLM працювати з власними документами й перевіряти відповіді за джерелами.

---

# Підсумковий проєкт модуля 2

## Document RAG Assistant

Після завершення модуля твій застосунок повинен мати таку архітектуру:

Evaluation і observability застосовуються до всіх етапів pipeline, а не лише до LLM.

## Рекомендована структура репозиторію

```

ai-knowledge-assistant/
├── src/
│   ├── api/
│   │   └── routes/
│   │       ├── documents.py
│   │       └── ask.py
│   ├── ingestion/
│   │   ├── loaders.py
│   │   ├── normalize.py
│   │   ├── chunking.py
│   │   └── pipeline.py
│   ├── embeddings/
│   │   └── encoder.py
│   ├── retrieval/
│   │   ├── dense.py
│   │   ├── sparse.py
│   │   ├── hybrid.py
│   │   └── reranker.py
│   ├── rag/
│   │   ├── context.py
│   │   ├── prompts.py
│   │   └── pipeline.py
│   └── llm/
├── evals/
│   ├── golden_dataset.json
│   ├── metrics.py
│   ├── run.py
│   └── reports/
├── tests/
│   ├── unit/
│   └── integration/
├── data/
│   └── sample_documents/
└── docker-compose.yml

```

## Definition of Done

Готовність до модуля 3

Перевірте всі 14 критеріїв завершення.

- Реалізовано ingestion PDF, DOCX та HTML
- Є нормалізація, chunking і metadata
- Повторний імпорт не створює дублікатів
- Документи індексуються в Qdrant
- Працює dense semantic search
- Реалізовано BM25 та hybrid search
- Є порівняння retrieval-конфігурацій
- Реалізовано reranking
- RAG повертає відповідь із джерелами
- Система обробляє питання без відповіді
- Є перевірка tenant isolation
- Підготовлено golden dataset із 50 питань
- Автоматично обчислюються retrieval metrics
- Є evaluation report і regression baseline

## Що потрібно засвоїти перед переходом до модуля 3

Після цього модуля ти повинен уміти пояснити, чому RAG може давати неправильні відповіді навіть із хорошою LLM, як chunking впливає на retrieval, чим dense search відрізняється від BM25, коли потрібен reranking і як відрізнити retrieval failure від generation failure.

Головний інженерний принцип модуля: RAG потрібно не просто реалізувати, а систематично вимірювати та покращувати.

Наступний модуль — AI Agents, Tool Calling, LangGraph, MCP та Context Engineering. У ньому перетворимо Document RAG Assistant на агента, який зможе обирати інструменти, виконувати багатокрокові задачі та працювати з пам'яттю діалогу.

---

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

---

# Фінальний проєкт усього курсу

## AI Knowledge Assistant — Production Edition

Тепер потрібно об'єднати результати всіх чотирьох модулів.

### Повна архітектура

## Функціональні вимоги

Готовий застосунок повинен:

- Завантажувати PDF, DOCX та HTML.
- Індексувати документи в Qdrant.
- Виконувати hybrid search із reranking.
- Генерувати відповіді з цитуванням джерел.
- Підтримувати agentic tool calling.
- Використовувати власний MCP Server.
- Зберігати стан розмови.
- Працювати через FastAPI.
- Підтримувати streaming.
- Мати authentication та tenant isolation.
- Записувати traces і usage metrics.
- Виконувати автоматизовані evaluations.
- Розгортатися через CI/CD на Cloud Run.

## Definition of Done

Готовність фінального проєкту

Перевірте всі 18 критеріїв готовності:

- FastAPI API працює асинхронно
- Реалізовано authentication та authorization
- Tenant isolation перевірено
- Працює SSE streaming
- Реалізовано rate limiting
- Timeouts і retries обмежені
- Є idempotency для write-операцій
- Проведено performance benchmark
- Вимірюється cost per successful task
- Реалізовано model routing
- Проведено security testing
- Додано structured logging і tracing
- Secrets не зберігаються в репозиторії
- Є CI/CD із тестами
- Сервіс розгорнуто на Cloud Run
- Виконано staging smoke tests
- Підготовлено rollback procedure
- Є deployment runbook



## Що ти знатимеш після завершення курсу

За 16 тижнів ти пройдеш шлях від базових принципів LLM до розробки й підтримки AI-системи, яка використовує власні дані, інструменти, агентну оркестрацію та production infrastructure.

Важливо, що результатом буде не просто демонстраційний чатбот, а повноцінний AI Engineering portfolio project, який можна показувати на технічних співбесідах, використовувати як основу власного продукту або розвивати далі.

Наступним логічним кроком стане поглиблення матеріалів: архітектурні кейси, production-приклади коду, повні лабораторні роботи з тестами, питання для самоперевірки та окремі завдання для підготовки до AI Engineer interview.

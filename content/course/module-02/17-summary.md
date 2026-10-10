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

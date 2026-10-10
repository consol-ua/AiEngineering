## Урок 12. RAG Patterns та архітектурні компроміси

### 12.1. Naive RAG

Найпростіша схема:

`Query → Vector Search → Top-K → LLM`

Переваги: мінімальна складність, швидка розробка.

Недоліки: обмежена якість для складних або неоднозначних запитів.

### 12.2. Advanced RAG

Може включати:

- Hybrid search.
- Reranking.
- Query rewriting.
- Context compression.
- Metadata filtering.
- Parent-child retrieval.

Не потрібно реалізовувати всі компоненти одночасно.

### 12.3. Multi-query RAG

Система генерує декілька пошукових формулювань одного питання, виконує retrieval та об'єднує результати.

Корисно, коли користувач використовує неоднозначні терміни.

Ризик — додаткові витрати й нерелевантні результати.

### 12.4. Agentic RAG

Агент самостійно визначає, коли потрібен пошук, які інструменти викликати та чи достатньо доказів.

Цей підхід детально розглядатимемо в модулі 3.

### 12.5. Типові помилки RAG

| Антипатерн                     | Чому це проблема                         |
| ------------------------------ | ---------------------------------------- |
| Усі документи в одному промпті | Витрати, шум, context overflow           |
| Лише vector search             | Слабший пошук точних термінів            |
| Відсутність metadata           | Неможливо надійно цитувати й фільтрувати |
| Немає перевірки прав доступу   | Ризик витоку даних                       |
| Занадто великий Top-K          | Зайвий контекст і latency                |
| Відсутність evaluation         | Немає доказів покращення                 |
| Відповідь за будь-яких умов    | Hallucinations                           |

### Лабораторна робота №7

Реалізуй endpoint `POST /ask`.

Приклад контракту:

```python
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

class SourceReference(BaseModel):
    chunk_id: str
    document_id: str
    page: int | None = None

class AskResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
    insufficient_context: bool
```

Реалізація повинна:

1. Приймати питання.
2. Виконувати retrieval.
3. За потреби виконувати reranking.
4. Формувати контекст.
5. Викликати LLM.
6. Перевіряти структуровану відповідь.
7. Повертати джерела.

Критерії завершення: RAG працює з власними документами; є негативні сценарії; система не повертає вигадані source IDs; права доступу перевіряються до передачі контексту моделі.

Матеріали: [LlamaIndex Documentation](https://docs.llamaindex.ai/), [LangChain Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval), [Building and Evaluating Advanced RAG Applications](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/).

# Тиждень 8. RAG Evaluations & Quality Engineering


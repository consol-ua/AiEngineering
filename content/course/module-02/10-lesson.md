## Урок 10. Context Engineering для RAG

### 10.1. Чому Top-K недостатньо

Навіть якщо retriever знайшов п'ять релевантних chunks, не варто просто об'єднувати їх у довільному порядку.

Контекст може містити дублікати, суперечливі версії документів або фрагменти без достатнього пояснення.

Context Assembly — етап підготовки знайдених даних до передачі LLM.

### 10.2. Context Budget

Потрібно враховувати:

```formula
T_total = T_instructions + T_history + T_retrieval + T_output
```

Загальний обсяг має відповідати обмеженням моделі й API.

Практичні правила:

- Резервуй токени для відповіді.
- Видаляй дублікати.
- Обмежуй кількість фрагментів.
- Зберігай source IDs.
- Не включай зайві документи лише тому, що вони поміщаються в контекст.
- Не змішуй інструкції системи з текстом документів.

### 10.3. Приклад побудови контексту

```python
from pydantic import BaseModel

class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    source: str
    page: int | None = None
    text: str

def build_context(chunks: list[RetrievedChunk]) -> str:
    parts = []
    for chunk in chunks:
        parts.append(
            f"[SOURCE_ID: {chunk.chunk_id}]\n"
            f"Document: {chunk.source}\n"
            f"Page: {chunk.page}\n"
            f"Content:\n{chunk.text}"
        )
    return "\n\n---\n\n".join(parts)
```

Це навчальний приклад. У production варто додати token budget, escaping, дедуплікацію та контроль версій документів.


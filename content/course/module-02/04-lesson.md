## Урок 4. Metadata, Deduplication та Idempotency

### 4.1. Навіщо потрібні metadata

Metadata дозволяє зрозуміти походження фрагмента, фільтрувати документи та перевіряти права доступу.

Приклад:

```python
from pydantic import BaseModel

class ChunkMetadata(BaseModel):
    document_id: str
    chunk_id: str
    source_uri: str
    page_number: int | None
    tenant_id: str
    document_version: str
    chunking_version: str
    embedding_model: str
```

### 4.2. Deduplication

Повторні документи збільшують витрати на embeddings, спотворюють пошукові результати та можуть призводити до повторення однакових фрагментів у контексті.

Для точних дублікатів можна використовувати SHA-256 checksum.

Для майже однакових документів можуть знадобитися text normalization, MinHash або інші алгоритми near-duplicate detection.

### 4.3. Idempotency

Ідемпотентність означає, що повторне виконання операції не створює додаткових небажаних змін.

Для ingestion можна використовувати стабільні ідентифікатори:

```formula
chunk_id = hash(document_id, version, chunk_index)
```

У production також потрібна стратегія видалення chunks, які більше не існують у новій версії документа.

### Лабораторна робота №5

Реалізуй `DocumentIngestionPipeline`, який:

1. Приймає PDF, DOCX та HTML.
2. Витягує текст і metadata.
3. Нормалізує текст.
4. Розбиває на chunks.
5. Виявляє точні дублікати.
6. Зберігає результат у JSONL.
7. Коректно обробляє повторний імпорт.

Критерії завершення: 20–30 документів успішно оброблено; повторний запуск не створює дублікатів; кожен chunk має джерело; тести покривають порожні, пошкоджені та повторні файли.

Матеріали: [Unstructured](https://docs.unstructured.io/), [PyMuPDF](https://pymupdf.readthedocs.io/), [LangChain Text Splitters](https://docs.langchain.com/oss/python/integrations/splitters).

# Тиждень 6. Embeddings, Vector Databases та Hybrid Search


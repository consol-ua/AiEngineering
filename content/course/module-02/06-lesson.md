## Урок 6. Vector Databases та Approximate Nearest Neighbor Search

### 6.1. Навіщо потрібна Vector Database

Якщо маємо 100 документів, можна порівняти query embedding з усіма embeddings послідовно.

Але якщо в системі мільйони фрагментів, повний перебір може стати надто дорогим.

Vector Database надає:

- Індексацію векторів.
- Швидкий пошук найближчих сусідів.
- Фільтрацію за metadata.
- Оновлення й видалення документів.
- Persistence та засоби масштабування.

У цьому курсі використовуватимемо Qdrant.

### 6.2. Exact Search vs ANN

Exact Nearest Neighbor шукає справді найближчі вектори за обраною метрикою, порівнюючи всі необхідні кандидати.

Approximate Nearest Neighbor (ANN) використовує індекс, який значно прискорює пошук, але іноді може пропускати найближчі результати.

Це компроміс між latency, використанням ресурсів і recall.

### 6.3. HNSW

HNSW (Hierarchical Navigable Small World) — поширений алгоритм ANN, який використовує багаторівневу графову структуру.

Пошук переходить між близькими вузлами графа, поступово наближаючись до релевантних векторів.

Основні параметри реалізацій HNSW можуть включати:

- `m` — кількість зв'язків у графі.
- `ef_construct` — ширина пошуку під час побудови індексу.
- `ef_search` або аналогічний параметр — ширина пошуку під час виконання запиту.

Збільшення цих значень часто покращує recall, але може підвищувати використання пам'яті, час індексації або latency.

### 6.4. Collections, Points та Payload

У Qdrant:

Collection — логічний набір векторів.

Point — запис, який містить ідентифікатор, вектор і додаткові дані.

Payload — metadata, наприклад `document_id`, `tenant_id`, `source`, `page`.

Payload особливо важливий для фільтрації за правами доступу.

### Приклад запуску Qdrant

```

docker run -d \
  --name qdrant \
  -p 127.0.0.1:6333:6333 \
  -p 127.0.0.1:6334:6334 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant

```

Прив'язка до `127.0.0.1` обмежує доступ локальним комп'ютером. Не відкривай Qdrant у публічний інтернет без належної автентифікації, мережевої ізоляції та TLS.

### Створення колекції та індексація

```python
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
texts = [
    "FastAPI використовується для створення API.",
    "Qdrant зберігає векторні представлення.",
    "RAG поєднує retrieval і генерацію.",
]
vectors = model.encode(texts, normalize_embeddings=True).tolist()
collection_name = "knowledge_base"
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=len(vectors[0]), distance=models.Distance.COSINE),
    )
# У наданому тексті points=[ обривався. Доповнено навчальний приклад.
client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(id=index, vector=vector, payload={"text": text})
        for index, (text, vector) in enumerate(zip(texts, vectors))
    ],
    wait=True,
)
```

### Виконання пошуку

```python
# Продовження попереднього прикладу: client, model і collection_name вже створені.
query = "Для чого потрібна векторна база?"
query_vector = model.encode(query, normalize_embeddings=True).tolist()
result = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=3,
    with_payload=True,
)
for point in result.points:
    print(point.score, (point.payload or {}).get("text"))
```

Це базова навчальна реалізація. У production потрібно додати стабільні IDs, фільтри доступу, versioning та контроль оновлення колекцій.

### Best Practices для Vector Database

- Створюй payload indexes для полів, які часто використовуються у фільтрах.
- Перевіряй права доступу під час пошуку, а не після генерації.
- Версіонуй embedding-модель та схему індексу.
- Передбачай повторну індексацію.
- Не використовуй similarity score як універсальну оцінку достовірності.
- Вимірюй ANN recall відносно exact-search baseline.
- Плануй backup і відновлення індексу.


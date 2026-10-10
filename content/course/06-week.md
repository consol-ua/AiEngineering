# Тиждень 6. Embeddings, Vector Databases та Hybrid Search

## Урок 5. Семантичний пошук і embeddings

### 5.1. Чим semantic search відрізняється від keyword search

Традиційний пошук намагається знайти документи, які містять слова із запиту або лексично близькі до них.

Наприклад, користувач запитує:

> Як відновити доступ до облікового запису?

А документ містить:

> Інструкція зі скидання пароля користувача.

Keyword search може не знайти достатньо точного збігу, тоді як semantic search здатний визначити змістову близькість.

Для цього використовується embedding-модель:

```formula
f: Text → ℝᵈ
```

Вона перетворює текст на вектор фіксованої розмірності.

Важливо: embeddings не є «закодованими фактами», які можна безпомилково відновити. Це представлення, оптимізовані для певних завдань.

### 5.2. Dense і Sparse Embeddings

Dense embeddings — вектори, у яких більшість компонентів мають ненульові значення. Вони добре підходять для семантичної близькості.

Sparse representations — розріджені вектори, у яких лише невелика частина компонентів ненульова. Вони часто використовуються для лексичного пошуку, зокрема через BM25 або навчені sparse-моделі.

| Характеристика       | Dense retrieval     | Sparse retrieval              |
| -------------------- | ------------------- | ----------------------------- |
| Синоніми             | Зазвичай сильніший  | Залежить від лексичного збігу |
| Точні ідентифікатори | Може помилятися     | Часто сильніший               |
| Нові терміни         | Залежить від моделі | Може знайти точний термін     |
| Інтерпретація збігів | Складніша           | Зазвичай простіша             |
| Індекс               | Векторний           | Інвертований або sparse       |

### 5.3. Cosine Similarity, Dot Product та Euclidean Distance

Для порівняння embeddings використовують різні метрики.

Cosine similarity:

```formula
cos(a,b) = (a·b) / (‖a‖ × ‖b‖)
```

Dot product:

```formula
a·b = Σᵢ aᵢbᵢ
```

Euclidean distance:

```formula
d(a,b) = √Σᵢ(aᵢ−bᵢ)²
```

Для L2-нормалізованих векторів cosine similarity і dot product дають однаковий порядок ранжування.

Best practices

- Перевіряй, яку метрику рекомендує embedding-модель.
- Для retrieval використовуй модель, навчання якої відповідає задачі пошуку.
- Не змінюй embedding-модель без плану переіндексації.
- Для українських документів тестуй якість саме українською.
- Окремо перевіряй пошук за кодами, датами, назвами продуктів та ідентифікаторами.

### Приклад embeddings

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
documents = [
    "Інструкція зі скидання пароля",
    "Налаштування мережевого підключення",
    "Правила оформлення відпустки",
]
vectors = model.encode(documents, normalize_embeddings=True)
query = "Як відновити доступ до акаунта?"
query_vector = model.encode(query, normalize_embeddings=True)
scores = vectors @ query_vector
for index in np.argsort(scores)[::-1]:
    print(documents[index], float(scores[index]))
```

Цей приклад реалізує точний пошук по невеликому набору векторів у пам'яті. Для великих колекцій потрібна пошукова інфраструктура.

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

## Урок 7. BM25, Hybrid Search та Rank Fusion

### 7.1. Чому одного semantic search недостатньо

Розглянемо запит:

> Знайди помилку `ERR_PAYMENT_1042`.

Embedding search може знайти документи про платежі, але не обов'язково той, який містить точний код.

Keyword search у цьому випадку часто ефективніший.

Тому production RAG нерідко використовує hybrid search.

### 7.2. BM25

BM25 — алгоритм лексичного ранжування, який оцінює документи з урахуванням частоти термінів, їхньої рідкісності та довжини документа.

Спрощена формула:

```formula
BM25(D,Q) = Σq∈Q IDF(q) × f(q,D)(k₁+1) / [f(q,D)+k₁(1−b+b|D|/avgdl)]
```

де:

- f(q,D) — частота терміна в документі.
- IDF(q) — інформативність терміна.
- |D| — довжина документа.
- `avgdl` — середня довжина документа.
- k_1 і b — параметри алгоритму.

### 7.3. Reciprocal Rank Fusion

RRF об'єднує результати декількох пошукових систем, використовуючи їхні позиції в рейтингу.

```formula
RRF(d) = Σr∈R 1 / (k + rank_r(d))
```

Перевага RRF у тому, що не потрібно безпосередньо порівнювати scores із різних retrieval-систем.

### Best Practices

- Використовуй hybrid search, коли запити містять як природну мову, так і точні терміни.
- Налаштовуй fusion на evaluation dataset.
- Не об'єднуй сирі BM25 і cosine scores без нормалізації або обґрунтованого методу fusion.
- Аналізуй окремо запити з ідентифікаторами, назвами та семантичними перефразуваннями.
- Порівнюй hybrid search з простим dense baseline.

## Урок 8. Reranking та Two-stage Retrieval

### 8.1. Що таке reranker

Retriever повинен швидко знайти достатньо хороший набір кандидатів.

Reranker повторно оцінює ці документи точнішим, але часто дорожчим способом.

Наприклад:

`Query → Retriever (Top-30) → Reranker → Top-5`

### 8.2. Bi-encoder vs Cross-encoder

Bi-encoder обчислює embeddings для запиту й документа окремо. Це дозволяє попередньо індексувати документи.

Cross-encoder обробляє запит і документ разом, що дозволяє детальніше оцінювати їхню відповідність.

Cross-encoder часто використовується для reranking, оскільки обчислення для кожної пари query-document дорожчі.

### Best Practices

- Спочатку виміряй якість без reranking.
- Додавай reranker, якщо є помилки ранжування.
- Обмежуй кількість кандидатів.
- Враховуй latency й обчислювальні витрати.
- Не очікуй, що reranker знайде документ, якого немає серед кандидатів retriever.

### Лабораторна робота №6

Створи три retrieval-конфігурації:

1. Dense search.
2. BM25.
3. Hybrid search із reranking.

Підготуй 30 тестових запитів: семантичні, точні терміни, коди помилок, назви документів та неоднозначні питання.

Порівняй Recall@5, MRR і latency.

Критерії завершення: працює Qdrant, індексовано щонайменше 300 chunks, є три retrieval-конфігурації та звіт із поясненням, яка з них краще підходить для твоїх даних.

Матеріали: [Qdrant Documentation](https://qdrant.tech/documentation/), [Sentence Transformers](https://www.sbert.net/), [Large Language Models with Semantic Search](https://www.deeplearning.ai/short-courses/large-language-models-semantic-search/).


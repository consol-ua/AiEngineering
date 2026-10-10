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

# Тиждень 7. Production RAG Pipeline


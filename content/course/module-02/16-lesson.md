## Урок 16. Golden Dataset, Regression Testing та Continuous Evaluation

### 16.1. Golden Dataset

Golden dataset — набір контрольних запитів із заздалегідь визначеними очікуваними результатами.

Для RAG він може містити:

```

{
  "question_id": "q-001",
  "question": "Як скинути пароль?",
  "relevant_document_ids": [
    "account-recovery"
  ],
  "expected_answer": "Використати форму відновлення.",
  "answerable": true,
  "category": "account_access"
}

```

Для питань без відповіді використовуй `answerable: false` і порожній набір релевантних документів. Такі кейси оцінюй окремими метриками abstention, а не звичайним Recall@K.

### 16.2. Як формувати dataset

Підготуй щонайменше 50 запитів:

| Категорія                       | Кількість |
| ------------------------------- | --------- |
| Прості фактологічні             | 15        |
| Семантичні перефразування       | 10        |
| Точні терміни та ідентифікатори | 10        |
| Багатокрокові питання           | 5         |
| Питання без відповіді           | 5         |
| Неоднозначні або суперечливі    | 5         |
| Разом                           | 50        |

Не підбирай запитання лише під ті документи, які твій retriever уже добре знаходить. Це призведе до завищених результатів.

### 16.3. Regression Testing

Кожна зміна chunking, embedding-моделі, retrieval-параметрів або промпту може змінити якість.

Тому після змін потрібно запускати evaluation і порівнювати результати з baseline.

Наприклад:

| Метрика      | Baseline | Нова версія |
| ------------ | -------- | ----------- |
| Recall@5    | 0,78     | 0,86        |
| MRR          | 0,71     | 0,79        |
| Faithfulness | 0,84     | 0,82        |
| p95 latency  | 1,8 с    | 2,6 с       |

Ілюстративні дані, не результати реального тестування.

У цьому прикладі retrieval покращився, але faithfulness трохи знизилася, а latency зросла. Не можна автоматично вважати нову версію кращою.

### 16.4. Quality Gates

Quality gate — критерій, який система повинна виконати перед релізом.

Приклад для навчального проєкту:

- Recall@5 ≥ 0,80 на питаннях із релевантними документами.
- Не більше 5% schema validation failures.
- Усі перевірки tenant isolation проходять.
- Відсутні критичні security failures.
- p95 latency не перевищує встановлений бюджет.

Пороги потрібно визначати на основі ризиків і вимог конкретного продукту. Для невеликого dataset зміни метрик можуть бути статистично нестабільними.

### Лабораторна робота №8

Створи автоматизований evaluation pipeline:

`Golden Dataset → RAG Pipeline → Metrics → Report → Regression Comparison`

Реалізуй:

1. Завантаження JSON dataset.
2. Запуск retrieval.
3. Обчислення Recall@K та MRR.
4. Генерацію відповіді.
5. Перевірку schema та source IDs.
6. Оцінювання groundedness.
7. Формування JSON/Markdown-звіту.
8. Порівняння з baseline.

Критерії завершення: 50 тестових запитів, автоматизований звіт, збережений baseline та опис щонайменше п'яти типових помилок системи.

Матеріали: [Ragas Documentation](https://docs.ragas.io/), [Langfuse](https://langfuse.com/docs), [Building and Evaluating Advanced RAG Applications](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/).


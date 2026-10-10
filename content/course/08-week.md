# Тиждень 8. RAG Evaluations & Quality Engineering

## Урок 13. Чому RAG потрібно оцінювати на декількох рівнях

У звичайному backend-застосунку unit tests перевіряють, чи повертає функція очікуваний результат.

У RAG потрібно оцінювати не лише програмну логіку, а й якість пошуку та генерації.

Тому доцільно розділити evaluation на три рівні.

1\. Retrieval Evaluation

Чи знайшли правильні документи?

2\. Generation Evaluation

Чи правильно LLM використала контекст?

3\. End-to-End Evaluation

Чи отримав користувач корисну й достовірну відповідь?

Наприклад, RAG може знайти правильний документ, але модель неправильно інтерпретує його. Це generation failure, а не retrieval failure.

І навпаки, LLM може дати правильну відповідь зі своїх параметричних знань, хоча retrieval не знайшов потрібного документа. Такий результат не означає, що RAG pipeline працює правильно.

## Урок 14. Retrieval Metrics

### 14.1. Recall@K

Recall@K вимірює, яку частку релевантних документів знайдено серед перших K результатів.

```formula
Recall@K = |Relevant ∩ Retrieved_K| / |Relevant|
```

Приклад: якщо для запиту є чотири релевантні chunks, а система знайшла три з них у Top-5, Recall@5 дорівнює 0,75.

### 14.2. Precision@K

Precision@K вимірює частку релевантних результатів серед перших K.

```formula
Precision@K = |Relevant ∩ Retrieved_K| / K
```

Високий Recall не завжди означає високу Precision.

### 14.3. Mean Reciprocal Rank

MRR оцінює позицію першого релевантного результату.

```formula
MRR = (1/N) Σᵢ 1/rankᵢ
```

Ця метрика корисна, коли достатньо знайти один правильний документ.

### 14.4. NDCG

Normalized Discounted Cumulative Gain враховує позиції документів і градації релевантності.

Вона корисна, коли одні документи є частково релевантними, а інші — повністю.

### Приклад Recall@K

```python
def recall_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    if not relevant_ids:
        raise ValueError("Recall is undefined without relevant docs")
    if k < 1:
        raise ValueError("k must be positive")
    retrieved = set(retrieved_ids[:k])
    return len(retrieved & relevant_ids) / len(relevant_ids)

score = recall_at_k(["a", "b", "c", "d"], {"b", "d", "e"}, 3)
print(score)  # 0.333...
```

## Урок 15. Generation Metrics, Faithfulness та LLM-as-a-Judge

### 15.1. Faithfulness

Faithfulness оцінює, чи підтверджуються твердження згенерованої відповіді наданим контекстом.

Це не тотожне фактичній правильності.

Відповідь може точно переказувати документ, який сам містить помилкову інформацію.

### 15.2. Answer Correctness

Answer correctness оцінює відповідність відповіді очікуваному результату.

Для цього можна використовувати:

- Exact match.
- Семантичне порівняння.
- Rule-based перевірки.
- Human evaluation.
- LLM-as-a-judge.

### 15.3. Context Relevance

Context relevance оцінює, наскільки retrieved chunks відповідають питанню.

Це допомагає виявляти випадки, коли retrieval знаходить формально схожі, але непотрібні документи.

### 15.4. LLM-as-a-Judge

Іншу LLM можна використовувати як оцінювача.

Наприклад, judge отримує питання, контекст, відповідь та рубрику:

```

Evaluate whether the answer is supported
by the provided context.

Score:
0 = Unsupported
1 = Partially supported
2 = Fully supported

Return:
- score
- explanation
- unsupported_claims

```

Best practices

- Калібруй judge на прикладах із людськими оцінками.
- Використовуй чітку рубрику.
- Зберігай версію judge-моделі.
- Перевіряй стабільність результатів.
- Не покладайся на одну автоматичну метрику.
- Окремо аналізуй критичні помилки.

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


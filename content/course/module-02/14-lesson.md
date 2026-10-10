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


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


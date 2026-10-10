## Урок 12. Context Engineering

### 12.1. Що таке Context Engineering

Context Engineering — проєктування інформації, яку модель отримує в момент виконання задачі.

Prompt Engineering переважно фокусується на формулюванні інструкцій.

Context Engineering охоплює ширшу задачу:

- Які документи передати.
- Яку історію розмови включити.
- Які інструменти зробити доступними.
- Які результати попередніх викликів зберегти.
- Як розподілити token budget.
- Які дані вважати довіреними.
- Як підтримувати актуальність контексту.

### 12.2. Context Window не дорівнює пам'яті

Навіть модель із великим context window може погано використовувати частину наданої інформації.

Проблеми:

Context dilution: важливі факти губляться серед нерелевантних даних.

Lost in the middle: інформація всередині довгого контексту може використовуватися гірше, ніж інформація на початку або наприкінці.

Context contamination: у контекст потрапляють суперечливі або недовірені інструкції.

Context overflow: обсяг перевищує ліміт моделі.

### 12.3. Context Budgeting

Припустимо, для певної конфігурації доступний бюджет 32 000 токенів.

Можна розподілити його так:

| Частина контексту | Бюджет токенів |
| --- | --- |
| System + tools | 3 000 |
| Conversation history | 6 000 |
| Retrieved context | 16 000 |
| Output + reserve | 7 000 |
| Разом | 32 000 |

Ілюстративний розподіл. Реальні ліміти залежать від моделі, API та особливостей задачі.

### 12.4. Context Selection Strategies

Recency-based selection: залишаємо найновіші повідомлення.

Relevance-based selection: вибираємо інформацію, найбільш пов'язану з поточним питанням.

Priority-based selection: резервуємо місце для критичних інструкцій і обмежень.

Summarization: стискаємо старі повідомлення.

Retrieval-based memory: знаходимо релевантні записи з довгострокової пам'яті.

Найкращий результат часто дає комбінація цих підходів.

### 12.5. Context Engineering Best Practices

1. Передавай тільки необхідну інформацію.
2. Зберігай походження даних.
3. Розмежовуй інструкції та недовірений контент.
4. Використовуй token-aware truncation.
5. Зберігай цілісність tool-call history.
6. Не стискай критичні факти без перевірки.
7. Вимірюй вплив контексту на якість.
8. Версіонуй правила формування контексту.

### Лабораторна робота №11

Завдання: реалізувати stateful Agentic RAG Assistant.

Функціональні вимоги:

- Підтримка декількох розмов.
- LangGraph checkpointing.
- Short-term memory.
- Summary memory.
- Пошук у документах.
- Повторний retrieval за необхідності.
- Контроль context budget.
- Tenant isolation.

Підготуй 30 тестових сценаріїв, включно з follow-up questions, довгими діалогами, неоднозначними запитами та відновленням після перезапуску.

Критерії перевірки: агент правильно використовує попередній контекст, не змішує розмови різних користувачів, не перевищує встановлений бюджет і не виконує нескінченних циклів.

### Безкоштовні матеріали тижня 11

- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) — checkpointing і стан.
- [LangGraph Memory](https://docs.langchain.com/oss/python/langgraph/add-memory) — пам'ять агентів.
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) — дослідження використання довгого контексту.
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — інженерні підходи до формування контексту.

# Тиждень 12. AI-assisted Development, Agent Evaluation & Reliability


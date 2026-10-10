# Модуль 4. Production AI Engineering, Security & Deployment

AI Engineering · Навчальний посібник · Тижні 13–16

У попередніх модулях ми розібрали принципи роботи LLM, створили RAG-систему та розширили її можливості за допомогою AI Agents, LangGraph і MCP.

Тепер переходимо від прототипу до production-ready AI-застосунку.

У цьому модулі розглянемо надійність API, оптимізацію витрат і швидкодії, безпеку LLM, observability, CI/CD та розгортання на Google Cloud Run.

Особливу увагу приділимо тому, що часто залишається поза межами AI-курсів: обробці збоїв, ізоляції користувачів, контролю витрат, тестуванню релізів і підтримці системи після deployment.

| Тривалість | Навантаження | Теорія | Практика |
| --- | --- | --- | --- |
| 4 тижні | 32 години | 12 годин | 20 годин |

Фінальний результат: production-версія AI Knowledge Assistant із FastAPI, Redis, Qdrant, LangGraph, MCP, observability, захистом від типових атак, автоматизованими тестами та deployment на Cloud Run.

## Програма модуля

| Тиждень | Тема                                | Результат                             |
| ------- | ----------------------------------- | ------------------------------------- |
| 13      | Production API & Reliability        | Стійкий до збоїв AI Backend           |
| 14      | LLM Optimization & Cost Engineering | Контроль latency, якості й витрат     |
| 15      | AI Security & Observability         | Захищений та спостережуваний pipeline |
| 16      | CI/CD, Cloud Run & Operations       | Розгорнутий AI-сервіс                 |

# Тиждень 13. Production API Architecture & Reliability


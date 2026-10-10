# Підсумковий проєкт модуля 1

## LLM Gateway + Document Classification

Об'єднай усі чотири тижні в один застосунок.

Мінімальна архітектура:

```
FastAPI
  |
  +-- POST /generate
  +-- POST /classify
  +-- POST /generate/stream
  |
LLM Gateway
  |
  +-- Ollama Provider
  +-- Cloud Provider
  |
Validation
  |
  +-- Pydantic
  +-- Prompt Versions
  +-- Metrics
```

## Definition of Done

Готовність до наступного модуля: перевірте всі 12 критеріїв.

- Розумію Transformer, attention, tokenization та inference
- Можу пояснити temperature, top-p, KV cache і context window
- Запустив і порівняв дві локальні LLM
- Реалізував LLMProvider abstraction
- Підключив Ollama та хмарний API
- Додав async requests, timeouts і retry
- Реалізував streaming
- Відстежую latency та використання токенів
- Створив версіоновані промпти
- Використовую Pydantic та structured outputs
- Маю щонайменше 30 evaluation cases
- Усі unit tests проходять без реальних API-запитів

## Як поглиблювати матеріал

Для системного навчання використовуй такий порядок: спочатку прочитай теорію уроку, потім переглянь рекомендоване відео або документацію, відтвори приклад коду, зміни його параметри й нарешті виконай лабораторну роботу без копіювання готового рішення.

Окремо веди `learning-notes.md`, де записуй не тільки визначення, а й результати експериментів, помилки та архітектурні рішення.

Після модуля 1 ти матимеш фундамент для наступного етапу — Data Ingestion, Embeddings, Vector Databases та RAG. Саме там навчимо LLM працювати з власними документами й перевіряти відповіді за джерелами.

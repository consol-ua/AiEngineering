## Урок 2. Async Processing, Background Jobs & Streaming

### 2.1. Async I/O

У FastAPI асинхронність корисна для операцій, які очікують відповіді від зовнішніх сервісів:

- LLM API.
- Qdrant.
- Redis.
- HTTP-інструменти.
- Бази даних з async-драйверами.

Але `async def` не робить CPU-bound операції автоматично неблокувальними.

Наприклад, локальна embedding-модель може виконувати важкі обчислення й блокувати event loop, якщо її викликати безпосередньо.

Для таких задач можуть знадобитися worker pool, окремі процеси або спеціалізований inference-сервіс.

### 2.2. BackgroundTasks vs Queue

FastAPI `BackgroundTasks` підходить для простих некритичних задач після HTTP-відповіді.

Але для тривалого ingestion великих PDF, embeddings або масової індексації краще використовувати надійну чергу.

| Характеристика               | BackgroundTasks      | Durable Queue              |
| ---------------------------- | -------------------- | -------------------------- |
| Простота                     | Висока               | Нижча                      |
| Переживає завершення процесу | Не гарантується      | За правильної конфігурації |
| Retries                      | Потрібно реалізувати | Часто підтримуються        |
| Масштабування workers        | Обмежене             | Гнучкіше                   |
| Великі ingestion jobs        | Небажано             | Рекомендовано              |

Для Google Cloud можна розглядати Cloud Tasks або Pub/Sub залежно від вимог.

### 2.3. Server-Sent Events

SSE дозволяє передавати події від сервера до клієнта через HTTP.

Приклад із FastAPI:

```python
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def generate_tokens():
    for token in ["Привіт", ", ", "світе!"]:
        payload = json.dumps({"token": token}, ensure_ascii=False)
        yield f"event: token\ndata: {payload}\n\n"
    yield "event: done\ndata: {}\n\n"

@app.get("/stream")
async def stream():
    return StreamingResponse(
        generate_tokens(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
```

Це демонстрація SSE-протоколу, а не реальний LLM streaming.

У production потрібно враховувати cancellation, client disconnect, backpressure, proxy buffering і завершення потоку з помилкою.

### Best Practices

- Не виконуй важкий CPU inference в event loop.
- Використовуй durable queue для критичних фонових задач.
- Не передавай секрети в SSE-подіях.
- Обмежуй кількість одночасних LLM-викликів.
- Коректно обробляй відключення клієнта.
- Передбачай окрему подію помилки в streaming-протоколі.


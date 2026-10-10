## Урок 11. LangGraph Persistence & Checkpointing

### 11.1. Навіщо потрібен checkpointing

Уявімо, що агент виконує багатокрокову задачу:

1. Знаходить документ.
2. Аналізує дані.
3. Викликає зовнішній API.
4. Очікує підтвердження.
5. Завершує операцію.

Якщо процес перезапуститься між третім і четвертим кроками, система повинна мати можливість відновити виконання.

Для цього використовують checkpointing.

### 11.2. Checkpointer у LangGraph

Для локальної розробки можна використати `InMemorySaver`.

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

def assistant_node(state: ChatState):
    return {"messages": [
        {"role": "assistant", "content": "Повідомлення отримано."}
    ]}

builder = StateGraph(ChatState)
builder.add_node("assistant", assistant_node)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
graph = builder.compile(checkpointer=InMemorySaver())
```

### 11.3. Thread ID

`thread_id` ідентифікує окрему історію виконання.

У реальному застосунку він повинен бути пов'язаний з авторизованим користувачем.

Не можна дозволяти користувачу отримувати чужу історію лише шляхом передавання іншого `thread_id`.

### 11.4. Production Persistence

`InMemorySaver` підходить для тестування, але не забезпечує надійного зберігання після перезапуску процесу.

Для production можна використовувати PostgreSQL-backed checkpointer або інше підтримуване постійне сховище.

### Best Practices

- Зберігай стан поза процесом застосунку.
- Перевіряй права доступу до thread.
- Використовуй стабільні ідентифікатори.
- Контролюй розмір checkpoint.
- Не зберігай секрети у відкритому вигляді.
- Плануй очищення старих сесій.
- Перевіряй відновлення після збою.


## Урок 4. LangGraph і Stateful Orchestration

### 4.1. Навіщо потрібен LangGraph

LangGraph — інструмент для побудови stateful workflow та агентних систем у вигляді графів.

Основні поняття:

State: поточні дані виконання.

Node: функція, яка читає стан і повертає його оновлення.

Edge: перехід між вузлами.

Conditional edge: вибір наступного вузла за умовою.

Checkpoint: збереження стану для відновлення або продовження виконання.

### 4.2. Приклад простого графа

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    question: str
    answer: str

def generate_answer(state: AgentState) -> dict:
    return {"answer": f"Отримано питання: {state['question']}"}

builder = StateGraph(AgentState)
builder.add_node("answer", generate_answer)
builder.add_edge(START, "answer")
builder.add_edge("answer", END)
graph = builder.compile()
# У наданому тексті graph.invoke обривався: завершено навчальний виклик.
result = graph.invoke({"question": "Що таке LangGraph?", "answer": ""})
print(result["answer"])
```

Це мінімальний приклад orchestration без LLM. Його мета — показати, як вузли читають та оновлюють стан.

### 4.3. Conditional Routing

У реальному агенті можна створити граф:

`START → Router → [Search | Calculate | Direct Answer] → Final Response`

Для складніших задач:

`START → Agent → Tools → Agent → ... → END`

### 4.4. Контроль циклів

Необхідно передбачити:

- Максимальну кількість кроків.
- Умови завершення.
- Обробку помилок інструментів.
- Deadline виконання.
- Можливість відновлення після збою.
- Обмеження загальних витрат.

### Лабораторна робота №9

Створи агента з трьома інструментами:

- `search_documents` — пошук у RAG.
- `calculate` — арифметичні операції.
- `get_current_date` — отримання поточної дати.

Використай LangGraph для керування виконанням.

Підготуй 20 тестових запитів і перевір, чи правильно агент обирає інструмент.

Критерії завершення: щонайменше 18 із 20 сценаріїв мають правильний tool routing; цикли обмежені; аргументи перевіряються; відсутні неавторизовані виклики.

### Матеріали тижня 9

- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/overview) — архітектура графів, стан і виконання.
- [AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) — навчальний курс із практичними прикладами.
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — фундаментальна стаття про поєднання reasoning та actions.

# Тиждень 10. Model Context Protocol (MCP)


# Тиждень 10. Model Context Protocol (MCP)

## Урок 5. Що таке MCP і яку проблему він вирішує

### 5.1. Проблема інтеграції AI з інструментами

Припустимо, ми створюємо AI-асистента, який повинен працювати з GitHub, Google Drive, PostgreSQL і внутрішньою базою знань.

Без стандартизованого підходу для кожної інтеграції потрібно окремо реалізувати:

- Опис доступних функцій.
- Механізм виклику.
- Передавання аргументів.
- Обробку результатів.
- Керування підключенням.
- Обробку помилок.

Model Context Protocol (MCP) — відкритий протокол для стандартизованої взаємодії AI-застосунків із зовнішніми можливостями та контекстом.

Його мета — зменшити кількість спеціалізованих інтеграцій між AI-клієнтами та інструментами.

### 5.2. Архітектура MCP

Host — застосунок, у якому працює AI-асистент.

Client — компонент, що підтримує з'єднання з конкретним MCP Server.

Server — програма, яка надає інструменти, ресурси та інші можливості.

Один Host може працювати з кількома MCP Server через окремі клієнтські підключення.

### 5.3. MCP не є моделлю

MCP не виконує inference, не навчає LLM і не визначає автоматично, чи безпечно виконувати певну дію.

Це протокол інтеграції. Логіка вибору інструмента залишається в AI-застосунку, а авторизація й виконання — у відповідних програмних компонентах.

## Урок 6. Tools, Resources і Prompts

### 6.1. Tools

Tools — операції, які MCP Server надає клієнту.

Наприклад:

```
search_documents(query, limit)
get_document(document_id)
create_issue(title, description)
```

Tool може мати побічні ефекти. Наприклад, `create_issue` створює новий запис у зовнішній системі.

### 6.2. Resources

Resources — дані, які сервер надає для використання як контекст.

Приклади:

```
docs://architecture/overview
config://application/settings
```

На концептуальному рівні різниця така: tool призначений для виконання операції, resource — для отримання певного контенту.

Але конкретний дизайн залежить від інтеграції: читання документа може бути реалізоване і як resource, і як tool.

### 6.3. Prompts

MCP Server може надавати шаблони промптів, які допомагають клієнту організувати певний сценарій.

Наприклад, шаблон для аналізу pull request або підготовки технічного звіту.

### 6.4. Transport

MCP підтримує різні механізми комунікації. Для навчання найпростіше почати зі stdio, коли Host запускає локальний процес MCP Server та обмінюється з ним повідомленнями через стандартні потоки.

Для віддалених інтеграцій використовується HTTP-based transport, зокрема Streamable HTTP.

### Best Practices

- Для локальних інструментів починай зі stdio.
- Для віддаленого MCP плануй authentication, authorization та мережевий захист.
- Не відкривай MCP Server без потреби в публічний інтернет.
- Не використовуй MCP як заміну внутрішньої бізнес-логіки.
- Відокремлюй read-only та write-операції.
- Уникай інструментів із надто широкими повноваженнями.

## Урок 7. Створення власного MCP Server на Python

### 7.1. FastMCP

Python SDK для MCP надає високорівневий API для створення серверів.

Для навчального проєкту створимо сервер із двома інструментами: арифметикою та отриманням списку документів.

Встановлення:

```

uv add "mcp[cli]"

```

Створимо файл `src/mcp_server/server.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("knowledge-tools")

@mcp.tool()
def calculate_sum(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b

@mcp.tool()
def list_documents() -> list[str]:
    """List available sample documents."""
    return ["architecture.md", "api-guide.md", "deployment.md"]

if __name__ == "__main__":
    mcp.run()
```

Запуск:

```

uv run python src/mcp_server/server.py

```

У режимі stdio сервер очікує протокольні повідомлення від клієнта, тому звичайний запуск у терміналі не створює інтерактивного чату.

Для тестування використовуй MCP Inspector або клієнт із SDK.

### 7.2. Чому docstrings важливі

Описи інструментів допомагають AI-застосунку зрозуміти їхнє призначення.

Поганий опис:

```
"""Search."""
```

Кращий опис:

```
"""Search indexed documents for passages
relevant to a natural-language question.
Returns matching passages and source IDs."""
```

Але docstring не є механізмом безпеки. Всі перевірки прав і параметрів мають виконуватися в коді.

## Урок 8. MCP Client, Discovery та Security

### 8.1. Підключення до MCP Server

У Python SDK можна створити клієнтську сесію та викликати інструмент.

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(
        command="uv",
        args=["run", "python", "src/mcp_server/server.py"],
    )
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(tools)
            result = await session.call_tool(
                "calculate_sum", arguments={"a": 10, "b": 25},
            )
            print(result)

# Додано точку входу для запуску навчального клієнта.
if __name__ == "__main__":
    asyncio.run(main())
```

### 8.2. Tool Discovery

MCP Client може отримати список інструментів та їхні схеми.

Це дозволяє будувати інтеграції без жорсткого прописування всіх tool definitions у коді Host.

Однак автоматичне discovery не означає, що кожному знайденому інструменту можна довіряти.

### 8.3. Основні ризики MCP

Tool poisoning: шкідливі або оманливі описи інструментів можуть впливати на поведінку моделі.

Excessive permissions: інструмент отримує більше доступу, ніж потрібно.

Data exfiltration: зовнішній сервер або інструмент отримує дані, які не повинен бачити.

Confused deputy: застосунок із широкими повноваженнями виконує дію від імені користувача без належної перевірки його прав.

### Security Best Practices

- Підключай лише довірені MCP Server.
- Використовуй allowlist інструментів.
- Перевіряй аргументи на серверному боці.
- Передавай мінімально необхідний контекст.
- Не надавай інструментам довгоживучі адміністративні токени без потреби.
- Відокремлюй credentials різних користувачів.
- Для write-операцій передбачай підтвердження.
- Записуй audit events.
- Обмежуй час виконання та обсяг результатів.

### Лабораторна робота №10

Створи MCP Server із трьома інструментами:

| Tool               | Призначення                          |
| ------------------ | ------------------------------------ |
| `list_documents`   | Повертає список доступних документів |
| `search_documents` | Шукає інформацію в Qdrant            |
| `calculate_sum`    | Виконує арифметичну операцію         |

Додай MCP Client, який отримує список інструментів та викликає їх.

Критерії завершення: сервер працює через stdio; клієнт виконує discovery; аргументи валідовані; пошук не повертає документи іншого користувача; помилки мають передбачувану структуру.

### Безкоштовні матеріали тижня 10

[MCP — Introduction](https://modelcontextprotocol.io/docs/getting-started/intro) — основи протоколу.

[Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — приклади серверів і клієнтів.

[MCP Inspector](https://modelcontextprotocol.io/docs/tutorials/inspector) — інструмент тестування MCP.


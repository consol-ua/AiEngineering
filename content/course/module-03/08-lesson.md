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

# Тиждень 11. Agentic RAG, Memory & Context Engineering


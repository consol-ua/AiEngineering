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


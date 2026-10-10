## Урок 8. Ollama та локальний inference

Ollama дозволяє запускати підтримувані моделі локально та працювати з ними через HTTP API.

Встановлення: [Ollama Download](https://ollama.com/download).

```

# Завантаження моделі
ollama pull llama3.2:3b

# Інтерактивний запуск
ollama run llama3.2:3b

# Список завантажених моделей
ollama list

```

Приклад Python-клієнта:

```python
import httpx

async def ask_local_llm(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
        )
        response.raise_for_status()
        return response.json()["response"]
```

### Best Practices для локального inference

Вибір моделі: починай з невеликої instruct-моделі та перевіряй її на конкретних задачах.

Версіонування: зберігай точний ідентифікатор і digest моделі, якщо потрібна відтворюваність.

Ізоляція: не відкривай локальний inference API в публічний інтернет без належного захисту.

Ресурси: контролюй RAM/VRAM, CPU/GPU utilization та concurrency.

Benchmark: окремо вимірюй cold start, TTFT, tokens/sec та end-to-end latency.

### Лабораторна робота №2

Створи `model_benchmark.py`, який порівнює дві локальні моделі.

Потрібно оцінити:

1. Якість української мови.
2. Виконання складних інструкцій.
3. Генерацію JSON.
4. Час відповіді.
5. Споживання пам'яті.
6. Стабільність повторних відповідей.

Критерії завершення: порівняно щонайменше дві моделі на однакових 20 запитах, сформовано CSV-звіт та короткий ADR із поясненням вибору моделі.

Матеріали: [Ollama Docs](https://docs.ollama.com/), [Hugging Face — Transformers](https://huggingface.co/learn/llm-course/chapter2/1), [Sentence Transformers](https://www.sbert.net/).

# Тиждень 3. LLM API Engineering


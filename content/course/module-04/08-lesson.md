## Урок 8. Local Inference, vLLM та Quantization

### 8.1. Hosted vs Self-hosted Inference

Hosted API зменшує операційне навантаження.

Self-hosted inference дає більше контролю над інфраструктурою, але потребує управління GPU, concurrency, scaling та оновленнями.

### 8.2. vLLM

vLLM — inference engine для запуску підтримуваних моделей із фокусом на ефективне обслуговування запитів.

Серед важливих концепцій:

- Continuous batching.
- KV cache management.
- PagedAttention.
- Паралельне обслуговування запитів.
- OpenAI-compatible API для підтримуваних сценаріїв.

### 8.3. Quantization

Quantization зменшує точність представлення ваг, а іноді й інших компонентів моделі.

Це може зменшити потребу в пам'яті, але вплив на швидкість та якість залежить від моделі, обладнання й runtime.

### 8.4. Коли варто self-host

Self-hosted inference може бути виправданим, якщо:

- Є достатній стабільний обсяг запитів.
- Потрібен контроль над середовищем виконання.
- Є специфічні вимоги до обробки даних.
- Економіка GPU-інфраструктури вигідніша за API.
- Команда готова підтримувати inference infrastructure.

### Лабораторна робота №14

Порівняй дві або три конфігурації inference.

Виміряй:

- p50/p95 latency.
- TTFT.
- Output tokens/sec.
- Вартість запиту.
- Якість на golden dataset.
- Частку помилок.
- Cost per successful task.

Побудуй простий model router для двох категорій запитів.

Критерії завершення: є benchmark report, обґрунтований вибір моделі та документовані trade-offs між якістю, latency й вартістю.

### Матеріали тижня 14

- [vLLM Documentation](https://docs.vllm.ai/)
- [Latency Optimization](https://platform.openai.com/docs/guides/latency-optimization)
- [Ollama Documentation](https://docs.ollama.com/)

# Тиждень 15. AI Security, Guardrails & Observability


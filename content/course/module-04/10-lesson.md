## Урок 10. OWASP LLM Top 10 & Defense in Depth

OWASP публікує перелік основних категорій ризиків для LLM-застосунків.

Серед важливих напрямів:

Prompt Injection: маніпулювання поведінкою моделі.

Sensitive Information Disclosure: розкриття конфіденційних даних.

Supply Chain Risks: небезпечні залежності, моделі або зовнішні інструменти.

Improper Output Handling: використання відповіді LLM без належної перевірки.

Excessive Agency: надання агенту надмірних повноважень.

Unbounded Consumption: неконтрольоване використання ресурсів і витрат.

### Defense in Depth

Захист має складатися з декількох незалежних рівнів.

1

Authentication & Authorization

2

Input Validation & Data Boundaries

3

Tool Permissions & Sandboxing

4

Output Validation

5

Rate Limits & Cost Budgets

6

Monitoring & Audit Logs

Навіть якщо модель неправильно інтерпретує інструкцію, інші рівні повинні запобігти небезпечній дії.

### Антипатерни

- «Не розкривай секрети» як єдиний механізм захисту.
- Виконання SQL або shell-команд, згенерованих LLM, без обмежень.
- Передавання API keys у контекст моделі.
- Довіра до всіх MCP Servers.
- Відсутність tenant isolation.
- Логування повних персональних даних без потреби.


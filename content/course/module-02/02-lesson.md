## Урок 2. Parsing PDF, DOCX та HTML

### 2.1. Чому парсинг складніший, ніж здається

Документ — не завжди послідовний текст.

PDF може містити дві колонки, таблиці, заголовки, зображення, колонтитули та текстові блоки з нестандартним порядком читання.

Якщо парсер неправильно відновить порядок тексту, chunking і retrieval працюватимуть із пошкодженим змістом.

### 2.2. PDF Processing

Для PDF із текстовим шаром можна використовувати PyMuPDF.

```python
from pathlib import Path
import pymupdf

def extract_pdf(path: Path) -> list[dict]:
    pages = []
    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text", sort=True).strip()
            if text:
                pages.append({"page": page_number, "text": text, "source": path.name})
    return pages
```

`sort=True` може покращити порядок читання для деяких документів, але не гарантує правильного відновлення складного layout.

Для сканованих PDF потрібен OCR. У production також варто перевіряти наявність текстового шару та якість витягування.

### 2.3. DOCX Processing

Для простих документів можна використовувати `python-docx`.

```python
from pathlib import Path
from docx import Document

def extract_docx(path: Path) -> str:
    document = Document(path)
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)
```

Цей приклад витягує лише параграфи. Для production потрібно окремо враховувати таблиці, порядок елементів та інші структурні дані.

### 2.4. HTML Processing

Для HTML важливо відокремити основний вміст від навігації, футера, меню й рекламних блоків.

Поширені інструменти: Beautiful Soup, Trafilatura, Unstructured.

### Best Practices для Parsing

- Зберігай оригінальний файл.
- Перевіряй MIME type, розмір та обмеження парсера.
- Використовуй checksum для виявлення дублікатів.
- Зберігай сторінку, розділ та інші координати джерела.
- Перевіряй якість тексту після extraction.
- Не застосовуй OCR до всіх PDF без потреби.
- Обмежуй ресурси для обробки недовірених документів.
- Не виконуй активний вміст або макроси з документів.

### Антипатерни

- Вважати `extract_text()` універсальним рішенням.
- Ігнорувати таблиці й багатоколонковий layout.
- Видаляти всю структуру документа під час очищення.
- Зберігати лише текст без source metadata.
- Завантажувати необмежені файли без контролю ресурсів.


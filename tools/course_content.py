"""Load editable introduction, lesson and summary files for the four modules."""
from pathlib import Path
import re

CONTENT = Path(__file__).resolve().parents[1] / 'content/course'
FILES = ['00-intro.md', *(f'{n:02}-lesson.md' for n in range(1, 17)), '17-summary.md']


def load_module(module, content_root=CONTENT):
    if module not in range(1, 5):
        raise ValueError(f'Unknown module: {module}')
    folder = Path(content_root) / f'module-{module:02}'
    actual = {p.name for p in folder.glob('*.md')}
    if actual != set(FILES):
        raise ValueError(f'{folder}: expected 18 Markdown files; missing={set(FILES)-actual}, extra={actual-set(FILES)}')
    parts = [(folder / name).read_text() for name in FILES]
    if not re.match(rf'^# Модуль {module}\.', parts[0]):
        raise ValueError(f'{folder}: invalid introduction heading')
    for number, part in enumerate(parts[1:17], 1):
        headings = re.findall(r'^## Урок (\d+)\. (.+)$', part, re.M)
        if len(headings) != 1 or int(headings[0][0]) != number:
            raise ValueError(f'{folder}/{FILES[number]}: expected lesson {number}')
    marker = '# Фінальний проєкт усього курсу' if module == 4 else f'# Підсумковий проєкт модуля {module}'
    if not parts[-1].startswith(marker):
        raise ValueError(f'{folder}: invalid summary heading')
    return parts


def module_source(module, content_root=CONTENT):
    # Keep the original separators, including weekly headings and lab sections.
    return ''.join(load_module(module, content_root))


def reader_chunks(module, content_root=CONTENT):
    parts = load_module(module, content_root)
    titles = ['Огляд · 4 тижні, 32 години']
    titles += [re.search(r'^## (Урок \d+\. .+)$', part, re.M)[1] for part in parts[1:17]]
    titles += ['Фінальний проєкт курсу і Definition of Done' if module == 4 else 'Підсумковий проєкт і Definition of Done']
    return [(title, re.sub(r'^# Тиждень \d+\..*\n', '', part, flags=re.M))
            for title, part in zip(titles, parts)]

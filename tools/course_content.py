"""Read the course from 18 editable files: introduction, 16 weeks, summary."""
from pathlib import Path
import re

CONTENT = Path(__file__).resolve().parents[1] / 'content/course'
FILES = ['00-intro.md', *(f'{n:02}-week.md' for n in range(1, 17)), '17-summary.md']


def load_course(content_root=CONTENT):
    folder = Path(content_root)
    actual = {p.name for p in folder.glob('*.md')}
    if actual != set(FILES) or any(p.is_dir() for p in folder.iterdir()):
        raise ValueError(f'{folder}: expected 18 Markdown files; missing={set(FILES)-actual}, extra={actual-set(FILES)}')
    parts = [(folder / name).read_text() for name in FILES]
    if not parts[0].startswith('# Вступ до курсу\n'):
        raise ValueError('Invalid course introduction heading')
    if not parts[-1].startswith('# Підсумок курсу\n'):
        raise ValueError('Invalid course summary heading')
    for week, part in enumerate(parts[1:17], 1):
        if not re.match(rf'^# Тиждень {week}\.', part):
            raise ValueError(f'{FILES[week]}: expected week {week}')
        lessons = re.findall(r'^## Урок (\d+)\. ', part, re.M)
        first = (week-1) % 4 * 4 + 1
        if lessons != [str(n) for n in range(first, first+4)]:
            raise ValueError(f'{FILES[week]}: expected lessons {first}–{first+3}')
        if len(re.findall(r'^### Лабораторна робота', part, re.M)) != 1:
            raise ValueError(f'{FILES[week]}: expected one lab')
    return parts


def module_source(module, content_root=CONTENT):
    if module not in range(1, 5):
        raise ValueError(f'Unknown module: {module}')
    parts = load_course(content_root)
    intros = re.split(r'\n---\n\n(?=# Модуль \d+\.)', parts[0].removeprefix('# Вступ до курсу\n\n'))
    summaries = re.split(r'\n---\n\n(?=# (?:Підсумковий проєкт модуля|Фінальний проєкт усього курсу))', parts[-1].removeprefix('# Підсумок курсу\n\n'))
    if len(intros) != 4 or len(summaries) != 4:
        raise ValueError('Introduction and summary must each contain all four modules')
    for number, (intro, summary) in enumerate(zip(intros, summaries), 1):
        marker = '# Фінальний проєкт усього курсу' if number == 4 else f'# Підсумковий проєкт модуля {number}'
        if not intro.startswith(f'# Модуль {number}.') or not summary.startswith(marker):
            raise ValueError(f'Invalid introduction or summary for module {number}')
    first = (module-1)*4+1
    return intros[module-1] + ''.join(parts[first:first+4]) + summaries[module-1]


def reader_chunks(module, content_root=CONTENT):
    source = module_source(module, content_root)
    marker = '# Фінальний проєкт усього курсу' if module == 4 else f'# Підсумковий проєкт модуля {module}'
    final = source.index(marker)
    lessons = list(re.finditer(r'^## (Урок \d+\. .+)$', source[:final], re.M))
    chunks = [('Огляд · 4 тижні, 32 години', source[:lessons[0].start()])]
    chunks += [(m[1], source[m.start():lessons[n+1].start() if n<15 else final]) for n,m in enumerate(lessons)]
    chunks += [('Фінальний проєкт курсу і Definition of Done' if module == 4 else 'Підсумковий проєкт і Definition of Done', source[final:])]
    return [(title, re.sub(r'^# Тиждень \d+\..*\n', '', part, flags=re.M)) for title,part in chunks]

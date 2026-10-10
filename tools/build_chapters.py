"""Generate static reader pages from authored content; no network or dependencies."""
from pathlib import Path
import html
import json
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from content.chapters import CHAPTERS

def esc(s):return html.escape(str(s),quote=True)
def p(s):return '<p>'+esc(s)+'</p>'
def items(values):return '<ul>'+''.join('<li>'+esc(value)+'</li>' for value in values)+'</ul>'
def pairs(values):return ''.join('<h3>'+esc(title)+'</h3>'+p(text) for title,text in values)
def diagram(labels):
    parts=['<svg viewBox="0 0 720 145" role="img" aria-label="'+esc(' → '.join(labels))+'"><title>'+esc(' → '.join(labels))+'</title>']
    for i,label in enumerate(labels):
        x=10+i*180
        words=label.split(' '); mid=max(1,len(words)//2)
        parts.append(f'<rect x="{x}" y="25" width="160" height="90" rx="12" fill="{ "#285a43" if i==3 else "#dfe9d6"}"/>')
        parts.append(f'<text x="{x+80}" y="64" text-anchor="middle" fill="{"white" if i==3 else "#285a43"}" font-size="12" font-family="system-ui"><tspan x="{x+80}">{esc(" ".join(words[:mid]))}</tspan><tspan x="{x+80}" dy="20">{esc(" ".join(words[mid:]))}</tspan></text>')
        if i<3:parts.append(f'<text x="{x+165}" y="78" fill="#285a43" font-size="18">→</text>')
    return ''.join(parts)+'</svg>'

HEADINGS=['Що будуємо і навіщо','Як це працює на прикладі','Нові слова простими словами','Розрахунок крок за кроком','Як з’єднані частини','Корисні звички та їхня ціна','Типові помилки й виправлення','Код: запускаємо та розбираємо','Перевірки та обробка помилок','Практика: зробіть самостійно','Як перевірити свою роботу','Що почитати й подивитися далі']
for index,c in enumerate(CHAPTERS):
    number=f'{index+1:02}'
    example=(ROOT/'docs/examples'/f'{number}.py').read_text()
    core,tests=example.split('class Tests',1)
    core=core.strip();tests='class Tests'+tests
    reading='<ul>'+''.join('<li><a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(name)+'</a><br><small>'+esc(url)+'</small></li>' for name,url in c['reading'])+'</ul>'
    sections=[
      '<h1>'+esc(c['title'])+'</h1><div class="callout"><strong>Після цього розділу ви зможете</strong>'+p(c['outcome'])+'</div>'+p(c['theory'][0])+p('Вам достатньо базового Python: функцій, списків, словників та винятків. Працюємо над одним помічником для інструкцій команди. Спочатку прочитайте приклад, потім запустіть маленький код, після цього виконайте власне завдання. Незрозуміле слово шукайте на сторінці «Нові слова простими словами».'),
      ''.join(p(t) for t in c['theory'][1:])+ '<div class="callout"><strong>Зупиніться на хвилину</strong>'+p(c['questions'][0])+'</div>',
      '<dl>'+''.join('<div class="term"><dt>'+esc(term)+'</dt><dd>'+esc(text)+'</dd></div>' for term,text in c['terms'])+'</dl>'+p('Не потрібно завчати визначення. Візьміть одне слово й поясніть його на прикладі нашого помічника. Запишіть у нотатках власне речення. Англійську назву залишено, щоб ви впізнали її в документації.'),
      '<div class="formula">'+esc(c['formula'])+'</div>'+p(c['worked'])+'<h3>Спробуйте змінити одне число</h3>'+p('Повторіть розрахунок на аркуші або в Python. Спочатку передбачте результат, потім перевірте. Важливо розуміти, що саме вимірює число: схожість, правильність, пам’ять чи час. Не всі ці показники можна порівнювати між собою.'),
      diagram(c['architecture'])+'<h3>'+esc(c['pattern'][0])+'</h3>'+p(c['pattern'][1])+'<h3>Пройдіть шлях одного питання</h3>'+p('Уявіть питання «Як підключити VPN?». Для кожного блока схеми скажіть: що він отримує, що робить і що передає далі. Потім повторіть для неправильного вводу. Так ви зрозумієте, де виникає помилка, замість шукати її в усьому проєкті одразу.'),
      pairs(c['practices'])+'<div class="callout">У кожної зручності є ціна. Додатковий пошук займає час, збереження даних потребує місця, перевірки додають код. Оберіть одну пораду й поясніть, від якої конкретної помилки вона захищає.</div>',
      pairs(c['antipatterns'])+'<h3>Як розібрати помилку</h3>'+p('Оберіть один випадок і відтворіть його на своїх навчальних даних. Запишіть три речі: що очікували, що отримали та чому. Виправте причину й повторіть той самий випадок. Додайте перевірку, щоб помилка не повернулася після наступної зміни.'),
      '<ol>'+''.join('<li>'+esc(step)+'</li>' for step in c['steps'])+'</ol><a class="download" href="../examples/'+number+'.py" download>Завантажити '+number+'.py — код і перевірки ↓</a>'+p('Збережіть файл у новій папці. Приклад працює на Python 3.12+ зі стандартною бібліотекою, без платних сервісів. Нижче його основна частина; спочатку розберемо, що роблять функції.')+'<pre><code>'+esc(core)+'</code></pre><h3>Що тут відбувається</h3>'+items(c['walkthrough'])+'<h3>Маленький запуск із відомим результатом</h3>'+p('Створіть demo.py у тій самій папці, де лежить '+number+'.py. Скопіюйте наступний код і виконайте python demo.py. runpy.run_path() завантажує функції зі збереженого файла; ви не повинні переписувати їх вручну.')+'<pre><code>'+esc(c['demo'])+'</code></pre><h3>Очікуваний результат</h3><pre><code>'+esc(c['expected'])+'</code></pre><h3>Змініть і перевірте</h3>'+p(c['try_it']),
      p('У завантаженому файлі вже є перевірки. Виконайте python '+number+'.py з його папки. Наприкінці має бути OK. Це означає, що перевірки прикладу пройшли, а не що весь майбутній помічник готовий.')+'<pre><code>'+esc(tests)+'</code></pre>'+p('assertEqual перевіряє рівність, assertTrue — істинність умови, assertRaises — очікувану помилку. Якщо перевірка не пройшла, прочитайте очікуване й отримане значення. Помилка на неправильному вводі часто є саме потрібною поведінкою.')+p('Підміна зовнішнього сервісу перевіряє ваш код без мережі. Якість справжньої моделі, роботу зовнішньої бази та швидкість на вашому обладнанні перевіряють окремо. У FastAPI перетворюйте очікувані помилки на зрозумілу відповідь користувачу.'),
      p(c['lab'])+'<h3>Кроки завдання</h3><ol>'+''.join('<li>'+esc(step)+'</li>' for step in c['lab_steps'])+'</ol><h3>Що показати після виконання</h3>'+items(c['deliverables'])+'<div class="callout">Почніть із мінімального варіанта. Частини з позначкою «додатково» не потрібні для першого успіху. Якщо зовнішня модель чи обладнання недоступні, виконайте незалежні кроки й запишіть, що саме ще не перевіряли.</div>',
      '<h3>Що перевірити кодом</h3>'+items(c['automatic'])+'<h3>Що перевірити своїми очима</h3>'+items(c['manual'])+'<h3>Як зрозуміти, що завдання виконане</h3><table class="rubric"><tr><th>Стан</th><th>Що вже зроблено</th></tr><tr><td>Почав</td><td>Прочитав і запустив готовий приклад.</td></tr><tr><td>Базову практику виконав</td><td>Виконав основні кроки на своїх даних та зберіг результати.</td></tr><tr><td>Можу пояснити</td><td>Перевірив неправильний випадок, пояснив причину та записав обмеження.</td></tr></table><h3>Запитання для самоперевірки</h3>'+items(c['questions']),
      reading+'<h3>Відео</h3><p><a href="'+esc(c['video'][1])+'" target="_blank" rel="noopener">'+esc(c['video'][0])+'</a></p>'+p('Почніть з одного джерела, а не відкривайте все одразу. Більшість документації англійською: шукайте вже пояснені тут терміни та мінімальний приклад. Посилання «Пошук» веде на видачу YouTube, де треба самостійно вибрати ролик.')+'<h3>Як читати документацію без перевантаження</h3>'+p('Знайдіть приклад, схожий на ваше завдання. Прочитайте, які дані він приймає, що повертає та що треба встановити. Звірте версію бібліотеки. Після читання поверніться до практики й застосуйте одну нову річ. Незрозуміле запишіть у нотатки як конкретне запитання.')
    ]
    toc=''.join(f'<a href="#page-{i+1}" data-page="{i}">{i+1:02}. {esc(title)}</a>' for i,title in enumerate(HEADINGS))
    body=''.join(f'<section class="page" id="page-{i+1}"><div class="eyebrow">РОЗДІЛ {number} · НАВЧАЛЬНА СТОРІНКА {i+1}/12</div>'+('' if i==0 else '<h2>'+esc(HEADINGS[i])+'</h2>')+text+'</section>' for i,text in enumerate(sections))
    nav=(f'<a href="{index:02}.html">← Попередній розділ</a>' if index else '<a href="../">← До програми</a>')+(f'<a href="{index+2:02}.html">Наступний розділ →</a>' if index<15 else '<a href="../">До програми →</a>')
    text='<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(c['title'])+' — AI Atelier</title><link rel="stylesheet" href="../chapter.css"></head><body data-module="'+str(index)+'"><header class="reader-header"><a href="../">◈ AI ATELIER · Програма</a><span>'+number+' / 16</span><button id="print">Друк / PDF</button></header><div class="reader-shell"><nav aria-label="Зміст розділу"><details open><summary>Зміст · 12 сторінок</summary>'+toc+'</details></nav><main>'+body+'<div class="reader-controls"><button id="previous">← Назад</button><span id="position" aria-live="polite"></span><button id="next">Далі →</button></div><button class="view-all" id="showAll">Показати весь розділ</button><section class="notes"><h2>Ваші результати й нотатки</h2>'+''.join(f'<label class="task"><input type="checkbox" data-step="{i}">{label}</label>' for i,label in enumerate(['Прочитав і можу пояснити основну ідею','Переглянув відео або зробив короткий конспект','Виконав основні кроки практики на своїх даних','Перевірив результат і неправильний випадок']))+'<label for="chapterNotes">Мої нотатки до розділу</label><textarea id="chapterNotes" rows="7" maxlength="20000" aria-describedby="noteStatus"></textarea><p class="status" id="noteStatus" role="status"></p><a href="../#backup">Експорт / імпорт резервної копії →</a></section><div class="chapter-nav">'+nav+'</div></main></div><script src="../chapter.js"></script></body></html>'
    (ROOT/'docs/chapters'/f'{number}.html').write_text(text)
with zipfile.ZipFile(ROOT/'docs/examples/all-examples.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for path in sorted((ROOT/'docs/examples').glob('*.py')):archive.write(path,path.name)
print('Built 16 chapters × 12 reading pages and example archive.')

# Dashboard and reader share the same authored explanations and tasks.
topics=[[c['title'],c['subtitle'],c['theory'][0],c['lab'],' '.join(c['automatic']),c['reading'][0][1],c['video'][0].removeprefix('Пошук: '),c['architecture']] for c in CHAPTERS]
exercises=[dict(steps=c['lab_steps'],deliverables=c['deliverables'],walkthrough=c['walkthrough'],expected=c['expected'],tryIt=c['try_it']) for c in CHAPTERS]
(ROOT/'docs/course.js').write_text('const topics = '+json.dumps(topics,ensure_ascii=False,indent=2)+';\nconst snippets = '+json.dumps([c['demo'] for c in CHAPTERS],ensure_ascii=False,indent=2)+';\nconst exercises = '+json.dumps(exercises,ensure_ascii=False,indent=2)+';\n')

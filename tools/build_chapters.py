"""Generate static reader pages from authored content; no network or dependencies."""
from pathlib import Path
import html
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

HEADINGS=['Постановка задачі й теорія','Механізми та межі','Термінологія','Формули й розрахунки','Архітектура та потоки даних','Best practices і компроміси','Антипатерни','Покрокова реалізація','Тести й обробка помилок','Самостійна лабораторна','Evaluation та самоперевірка','Додаткове читання й відео']
for index,c in enumerate(CHAPTERS):
    number=f'{index+1:02}'
    example=(ROOT/'docs/examples'/f'{number}.py').read_text()
    core,tests=example.split('class Tests',1)
    core=core.strip();tests='class Tests'+tests
    reading='<ul>'+''.join('<li><a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(name)+'</a><br><small>'+esc(url)+'</small></li>' for name,url in c['reading'])+'</ul>'
    sections=[
      '<h1>'+esc(c['title'])+'</h1><div class="callout"><strong>Результат навчання</strong>'+p(c['outcome'])+'</div>'+p(c['theory'][0])+p('Цей розділ продовжує наскрізний проєкт асистента документації. Перед початком відкрийте свою попередню реалізацію й перевірте її тести. Запишіть у нотатках, яку поведінку ви очікуєте змінити, які дані потрібні та як будете перевіряти результат. Не відмічайте практичний крок лише за фактом прочитання прикладу: він вимагає власного виконання й артефактів лабораторної.'),
      ''.join(p(t) for t in c['theory'][1:])+ '<div class="callout"><strong>Перевірте розуміння</strong>'+p(c['questions'][0])+'</div>',
      '<dl>'+''.join('<div class="term"><dt>'+esc(term)+'</dt><dd>'+esc(text)+'</dd></div>' for term,text in c['terms'])+'</dl>'+p('Складіть власний мінісловник: для кожного терміна наведіть приклад із вашого проєкту та один близький термін, із яким його легко переплутати. Пояснення має бути зрозумілим розробнику, який знає Python, але ще не працював із цим компонентом. Якщо можете повторити визначення, але не навести контрприклад, поверніться до механізму на попередній сторінці.'),
      '<div class="formula">'+esc(c['formula'])+'</div>'+p(c['worked'])+p('Розрахуйте приклад вручну до запуску коду. Потім змініть одне припущення та запишіть, який результат очікуєте. Перевірка крайніх випадків важливіша за красиву формулу: визначте область допустимих значень, поведінку на порожньому вході та спосіб обробки невідомого результату. Формула спрощує систему; не використовуйте її як гарантію поведінки на даних, яких ви не виміряли.'),
      diagram(c['architecture'])+'<h3>'+esc(c['pattern'][0])+'</h3>'+p(c['pattern'][1])+p('Пройдіть схему зліва направо на одному нормальному й одному невдалому запиті. Для кожної стрілки запишіть формат даних, власника, межу довіри та можливий exception. Визначте, який компонент відповідає за retry, а який — за відмову. Не додавайте дубльовані перевірки без пояснення: незалежні security gates корисні, але два неузгоджені парсери можуть створити різну поведінку.')+ '<h3>Архітектурне рішення</h3>'+p('У нотатках створіть короткий ADR: контекст, обраний варіант, альтернатива, наслідки та спосіб перевірки. Якщо навантаження, corpus або модель зміняться, які припущення перестануть бути справедливими? ADR потрібен, щоб майбутня зміна була свідомим рішенням, а не повторенням чужого патерну.'),
      pairs(c['practices'])+ '<div class="callout">Оберіть одну рекомендацію, яка збільшує latency або складність, і поясніть, який ризик вона зменшує. «Завжди краще» не є достатнім обґрунтуванням.</div>',
      pairs(c['antipatterns'])+'<h3>Розбір інциденту</h3>'+p('Оберіть одну типову помилку й відтворіть її у контрольованому тесті з локальними даними. Запишіть симптом, першопричину, наслідок для користувача та regression test. Потім виправте реалізацію й доведіть, що тест відрізняє неправильну версію від правильної. Не вимикайте assertion, щоб отримати зелений результат: це прибирає доказ, а не помилку.'),
      '<ol>'+''.join('<li>'+esc(step)+'</li>' for step in c['steps'])+'</ol><a class="download" href="../examples/'+number+'.py" download>Завантажити повний виконуваний приклад '+number+'.py ↓</a>'+p('Нижче — повний core навчального компонента. Він використовує стандартну бібліотеку Python 3.12+, щоб ви могли перевірити логіку без API-ключів. Це baseline конкретної стадії, а не готовий production-сервіс. Інтеграція реальної моделі та зовнішніх залежностей описана у лабораторній.')+'<pre><code>'+esc(core)+'</code></pre>',
      p('Завантажений файл містить наведені нижче тести. Запустіть його у терміналі командою python '+number+'.py. Ненульовий exit code означає невдачу. Для негативних тестів спершу передбачте помилку, потім виконайте запуск. Успішний fake-тест перевіряє контракт і control flow, але не якість моделі, реальну мережу чи достатність hardware.')+'<pre><code>'+esc(tests)+'</code></pre>'+p('Для інтеграції додайте тест межі компонента: замість мокання всього pipeline підмініть лише зовнішню залежність. В API відображайте очікувані помилки на стабільний статус і коротке повідомлення; внутрішній traceback залишається у захищеній діагностиці без секретів.'),
      p(c['lab'])+'<h3>Порядок самостійної роботи</h3>'+items(['До реалізації: запишіть гіпотезу, вхідні дані та критерій успіху.', 'Перший прохід: запустіть baseline й збережіть результати без прикрашання.', 'Другий прохід: змініть один фактор і повторіть перевірку на тих самих даних.', 'Завершення: підготуйте артефакти, поясніть невдачі та додайте regression tests.'])+p('Не копіюйте приклад без змін як завершену лабораторну. Використайте власні дані та принаймні один крайній випадок, якого немає у прикладі. Якщо зовнішня залежність недоступна, завершіть незалежні кроки й позначте конкретну інтеграційну перевірку unrun. Це чесніше, ніж підмінити її тривіальним успіхом.'),
      '<h3>Автоматичні перевірки</h3>'+items(c['automatic'])+'<h3>Ручна оцінка</h3>'+items(c['manual'])+'<h3>Рубрика лабораторної</h3><table class="rubric"><tr><th>Рівень</th><th>Доказ</th></tr><tr><td>Не завершено</td><td>Є лише читання або незапущений код.</td></tr><tr><td>Базовий</td><td>Baseline і негативні тести виконані; результати збережені.</td></tr><tr><td>Повний</td><td>Власна лабораторна, порівняння, ручна перевірка та опис меж.</td></tr></table><h3>Запитання для самоперевірки</h3>'+items(c['questions']),
      reading+'<h3>Відео</h3><p><a href="'+esc(c['video'][1])+'" target="_blank" rel="noopener">'+esc(c['video'][0])+'</a></p>'+p('Посилання з позначкою «Пошук» ведуть на тематичну видачу YouTube, а не на перевірений конкретний ролик. Для навчання обирайте матеріал, де пояснюють механізм і демонструють результат, а не лише рекламують інструмент. Документації оновлюються: звіряйте API з установленою версією. Зовнішні сторінки й відео в цій роботі не перевірялися на доступність.')+'<h3>Як працювати з джерелами</h3>'+p('Спочатку прочитайте офіційне визначення й мінімальний приклад. Потім поверніться до вашого коду та перевірте припущення: типи входу, ліміти, exceptions і version compatibility. У нотатках збережіть URL, дату перегляду й одне рішення, яке змінили після читання. Відео — допоміжне пояснення; оцінку лабораторної визначають виконані перевірки й власні артефакти.')
    ]
    toc=''.join(f'<a href="#page-{i+1}" data-page="{i}">{i+1:02}. {esc(title)}</a>' for i,title in enumerate(HEADINGS))
    body=''.join(f'<section class="page" id="page-{i+1}"><div class="eyebrow">РОЗДІЛ {number} · НАВЧАЛЬНА СТОРІНКА {i+1}/12</div>'+('' if i==0 else '<h2>'+esc(HEADINGS[i])+'</h2>')+text+'</section>' for i,text in enumerate(sections))
    nav=(f'<a href="{index:02}.html">← Попередній розділ</a>' if index else '<a href="../">← До програми</a>')+(f'<a href="{index+2:02}.html">Наступний розділ →</a>' if index<15 else '<a href="../">До програми →</a>')
    text='<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(c['title'])+' — AI Atelier</title><link rel="stylesheet" href="../chapter.css"></head><body data-module="'+str(index)+'"><header class="reader-header"><a href="../">◈ AI ATELIER · Програма</a><span>'+number+' / 16</span><button id="print">Друк / PDF</button></header><div class="reader-shell"><nav aria-label="Зміст розділу"><details open><summary>Зміст · 12 сторінок</summary>'+toc+'</details></nav><main>'+body+'<div class="reader-controls"><button id="previous">← Назад</button><span id="position" aria-live="polite"></span><button id="next">Далі →</button></div><button class="view-all" id="showAll">Показати весь розділ</button><section class="notes"><h2>Ваші результати й нотатки</h2>'+''.join(f'<label class="task"><input type="checkbox" data-step="{i}">{label}</label>' for i,label in enumerate(['Теорію й джерела опрацьовано','Відео або конспект опрацьовано','Власну лабораторну виконано','Критерії перевірено']))+'<label for="chapterNotes">Мої нотатки до розділу</label><textarea id="chapterNotes" rows="7" maxlength="20000" aria-describedby="noteStatus"></textarea><p class="status" id="noteStatus" role="status"></p><a href="../#backup">Експорт / імпорт резервної копії →</a></section><div class="chapter-nav">'+nav+'</div></main></div><script src="../chapter.js"></script></body></html>'
    (ROOT/'docs/chapters'/f'{number}.html').write_text(text)
with zipfile.ZipFile(ROOT/'docs/examples/all-examples.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for path in sorted((ROOT/'docs/examples').glob('*.py')):archive.write(path,path.name)
print('Built 16 chapters × 12 reading pages and example archive.')

from build_module1 import build as build_module1
build_module1()

build_module1(2)

build_module1(3)

build_module1(4)

# Single downloadable handbook, assembled without changing module content.
modules=[(ROOT/f'content/module{number}.md').read_text().rstrip() for number in range(1,5)]
handbook='# AI Engineering — повний посібник\n\nУсі 4 модулі · 16 тижнів · 64 уроки · 16 лабораторних робіт.\n\n'+ '\n\n---\n\n'.join(modules)+'\n'
(ROOT/'docs/ai-engineering-full-course.md').write_text(handbook)
print('Built complete four-module handbook.')

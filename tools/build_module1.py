"""Render supplied Module 1 Markdown, preserving all 16 lessons and labs.
Called by build_chapters.py after the shared reader shell is generated.
"""
from pathlib import Path
import html
import re

ROOT=Path(__file__).resolve().parents[1]

def inline(text):
    tokens=[]
    def token(value):
        index=len(tokens);tokens.append(value);return f'\x00{index}\x00'
    text=re.sub(r'`([^`]+)`',lambda m:token('<code>'+html.escape(m[1])+'</code>'),text)
    text=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',lambda m:token('<a href="'+html.escape(m[2],quote=True)+'" target="_blank" rel="noopener">'+html.escape(m[1])+'</a>'),text)
    text=html.escape(text)
    return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m[1])],text)

def render(source):
    lines=source.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            kind=line[3:].strip();code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            i+=1
            if kind=='formula':out.append('<div class="formula">'+html.escape('\n'.join(code))+'</div>')
            else:out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>')
            continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',c.replace(' ','')) for c in cells):rows.append(cells)
                i+=1
            out.append('<div class="table-scroll"><table class="rubric">'+''.join('<tr>'+''.join('<'+('th' if n==0 else 'td')+'>'+inline(cell)+'</'+('th' if n==0 else 'td')+'>' for cell in cells)+'</tr>' for n,cells in enumerate(rows))+'</table></div>');continue
        match=re.match(r'^(#{1,6})\s+(.+)$',line)
        if match:
            level=min(4,len(match[1])+1)
            out.append(f'<h{level}>'+inline(match[2])+f'</h{level}>');i+=1;continue
        if re.match(r'^(?:- |\d+\. )',line):
            ordered=bool(re.match(r'^\d+\. ',line));tag='ol' if ordered else 'ul';li=[]
            while i<len(lines) and re.match(r'^(?:\d+\. )' if ordered else r'^- ',lines[i]):
                li.append('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',lines[i]))+'</li>');i+=1
            out.append('<'+tag+'>'+''.join(li)+'</'+tag+'>');continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(?:#|```|\||- |\d+\. )',lines[i]):paragraph.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return ''.join(out)

def build():
    source=(ROOT/'content/module1.md').read_text()
    final=source.index('# Підсумковий проєкт модуля 1')
    body=source[:final]
    lessons=list(re.finditer(r'^## Урок (\d+)\. (.+)$',body,re.M))
    assert len(lessons)==16
    intro=body[:lessons[0].start()]
    intro=re.sub(r'^# Тиждень 1\..*\n','',intro,flags=re.M)
    chunks=[('Огляд · 4 тижні, 32 години',intro)]
    weeks=[]
    for n,match in enumerate(lessons):
        part=body[match.start():lessons[n+1].start() if n+1<len(lessons) else len(body)]
        part=re.sub(r'^# Тиждень \d+\..*\n','',part,flags=re.M)
        chunks.append((f'Урок {n+1}. {match[2]}',part))
    chunks.append(('Підсумковий проєкт і Definition of Done',source[final:]))
    path=ROOT/'docs/chapters/01.html'
    old=path.read_text()
    toc=''.join(f'<a href="#page-{n+1}" data-page="{n}">{n+1:02}. {html.escape(title)}</a>' for n,(title,_) in enumerate(chunks))
    old=re.sub(r'<details open>.*?</details>','<details open><summary>Зміст · 18 сторінок</summary>'+toc+'</details>',old,count=1,flags=re.S)
    pages=[]
    for n,(title,part) in enumerate(chunks):
        week=f' · ТИЖДЕНЬ {(n-1)//4+1}' if 1<=n<=16 else ''
        extra=''
        if n==0:
            extra='<div class="callout">Модуль 1 · 4 тижні · 32 години (12 теорія + 20 практика). Наявні нотатки та 4 відмітки прогресу збережено.</div><p><a href="../module1.md" download>Завантажити текст модуля у Markdown ↓</a></p>'
        if n==9:
            extra='<h3>Схема LLM Gateway</h3><svg viewBox="0 0 720 120" role="img" aria-label="FastAPI → Gateway → Ollama або Cloud → Validation"><rect x="5" y="25" width="150" height="65" rx="10" fill="#dfe9d6"/><text x="80" y="64" text-anchor="middle">FastAPI</text><text x="162" y="64">→</text><rect x="185" y="25" width="150" height="65" rx="10" fill="#dfe9d6"/><text x="260" y="64" text-anchor="middle">Gateway</text><text x="342" y="64">→</text><rect x="365" y="25" width="150" height="65" rx="10" fill="#dfe9d6"/><text x="440" y="64" text-anchor="middle">Ollama / Cloud</text><text x="522" y="64">→</text><rect x="545" y="25" width="170" height="65" rx="10" fill="#dfe9d6"/><text x="630" y="64" text-anchor="middle">Validation</text></svg>'
        pages.append(f'<section class="page" id="page-{n+1}"><div class="eyebrow">МОДУЛЬ 1{week} · СТОРІНКА {n+1}/18</div>'+extra+render(part)+'</section>')
    start=old.index('<main>')+len('<main>');end=old.index('<div class="reader-controls">',start)
    old=old[:start]+''.join(pages)+old[end:]
    old=re.sub(r'<title>.*?</title>','<title>LLM Foundations &amp; Prompt Engineering — AI Atelier</title>',old,count=1)
    old=old.replace('data-module="0"','data-module="0" data-extended="true"')
    path.write_text(old)
    (ROOT/'docs/module1.md').write_text(source)
    print('Updated Module 1: 16 lessons, 4 labs, final project, 18 reader pages.')

if __name__=='__main__':build()

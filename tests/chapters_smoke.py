"""Browser/readiness test: CHROMIUM_PATH=/usr/bin/chromium python tests/chapters_smoke.py."""
import functools
import ast
import re
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/docs/'
try:
    module_source=(ROOT/'content/module1.md').read_text()
    samples=re.findall(r'```python\n(.*?)\n```',module_source,re.S)
    assert len(samples)==5
    for sample in samples:ast.parse(sample)
    assert len(re.findall(r'^## Урок ',module_source,re.M))==16
    assert len(re.findall(r'^### Лабораторна робота',module_source,re.M))==4
    for example in sorted((ROOT/'docs/examples').glob('*.py')):
        result=subprocess.run([sys.executable,str(example)],capture_output=True,text=True)
        assert result.returncode==0,(example,result.stderr)
    with sync_playwright() as p:
        opts={'headless':True}
        if os.getenv('CHROMIUM_PATH'):opts['executable_path']=os.environ['CHROMIUM_PATH']
        browser=p.chromium.launch(**opts)
        context=browser.new_context(accept_downloads=True)
        page=context.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        counts=[]
        for i in range(16):
            page.goto(base+f'chapters/{i+1:02}.html')
            expected=18 if i==0 else 12
            assert page.locator('.page').count()==expected
            assert page.locator('.page:visible').count()==1
            assert page.locator('nav a[data-page]').count()==expected
            page.locator('#next').click()
            assert page.locator('#page-2').is_visible()
            page.locator('#showAll').click()
            assert page.locator('.page:visible').count()==expected
            page.locator('#showAll').click()
            # Print mode must include all pages, even when reader shows only one.
            pdf=page.pdf(format='A4',prefer_css_page_size=True)
            document=PdfReader(io.BytesIO(pdf))
            count=len(document.pages)
            assert 10<=count<=20,(i+1,count)
            extracted='\n'.join(p.extract_text() for p in document.pages)
            assert 'Evaluation' in extracted and ('Best Practices' if i==0 else 'Best practices') in extracted
            counts.append(count)
            page.set_viewport_size({'width':390,'height':844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),i+1
            page.set_viewport_size({'width':1280,'height':900})
        page.goto(base+'chapters/01.html')
        page.locator('#showAll').click()
        for text in ['Урок 16.', 'Лабораторна робота №4', 'LLM Gateway', '32 години', '90% schema-valid']:
            assert text in page.locator('main').inner_text(),text
        assert page.locator('.formula').count()==6
        assert 'images.openai.com' not in page.content()
        page.locator('#chapterNotes').fill('Спільна нотатка <b>не HTML</b>')
        page.locator('[data-step="0"]').check()
        page.reload()
        assert page.locator('#chapterNotes').input_value().startswith('Спільна нотатка')
        assert page.locator('[data-step="0"]').is_checked()
        page.goto(base)
        assert page.locator('#progressText').inner_text()=='1 із 64 кроків'
        page.locator('.module').first.click()
        assert page.locator('#moduleNotes').input_value()=='Спільна нотатка <b>не HTML</b>'
        page.locator('#moduleNotes').fill('Оновлено з головної')
        page.locator('.chapter-link').click()
        assert page.locator('#chapterNotes').input_value()=='Оновлено з головної'
        page.locator('.notes a').click()
        assert page.locator('#backupView').is_visible()
        with page.expect_download() as event:page.locator('#exportButton').click()
        data=json.loads(Path(event.value.path()).read_text())
        assert data['notes']['0']=='Оновлено з головної'
        assert data['completed']==[0]
        assert not errors,errors
        print('PASS: 16 readers, 32 example tests, navigation, mobile, shared progress/notes and export.')
        print('A4 PDF page counts:',counts)
        context.close();browser.close()
finally:
    server.shutdown()

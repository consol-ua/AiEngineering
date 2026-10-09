"""Run with python tests/pages_smoke.py; requires Playwright and Chromium."""
import functools
import json
import os
from pathlib import Path
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/docs/'
try:
    with sync_playwright() as p:
        options = {'headless': True}
        if os.getenv('CHROMIUM_PATH'):
            options['executable_path'] = os.environ['CHROMIUM_PATH']
        browser = p.chromium.launch(**options)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        errors, requests = [], []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('request', lambda r: requests.append(r.url))
        page.goto(url)
        assert page.locator('.module').count() == 16
        page.locator('.module').first.click()
        page.locator('#tasks input').first.check()
        page.locator('#moduleNotes').fill('Моя нотатка <script> — українською\nДругий рядок')
        page.reload()
        assert page.locator('#progressText').inner_text() == '1 із 64 кроків'
        page.locator('.module').first.click()
        assert page.locator('#moduleNotes').input_value() == 'Моя нотатка <script> — українською\nДругий рядок'
        page.locator('#lessonDialog .close').click()
        page.locator('#backupNav').click()
        with page.expect_download() as event:
            page.locator('#exportButton').click()
        backup = json.loads(Path(event.value.path()).read_text())
        assert backup['completed'] == [0] and backup['version'] == 1
        assert backup['notes']['0'].startswith('Моя нотатка <script>')
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'backup.json'
            backup['completed'] = [7, 63]
            backup['notes'] = {'0': 'Імпортований висновок', '15': 'Фінальна нотатка'}
            path.write_text(json.dumps(backup))
            page.locator('#importFile').set_input_files(path)
            page.locator('#importButton').click()
            page.wait_for_function("document.getElementById('progressText').textContent==='3 із 64 кроків'")
            assert 'Імпортований висновок' in json.loads(page.evaluate("localStorage.getItem('ai-atelier.progress.v1')"))['notes']['0']
            assert 'Моя нотатка' in json.loads(page.evaluate("localStorage.getItem('ai-atelier.progress.v1')"))['notes']['0']
            legacy = dict(backup)
            legacy.pop('notes')
            path.write_text(json.dumps(legacy))
            page.locator('#importFile').set_input_files(path)
            page.locator('#importButton').click()
            page.wait_for_function("document.getElementById('backupStatus').textContent.includes('Відновлено')")
            assert json.loads(page.evaluate("localStorage.getItem('ai-atelier.progress.v1')"))['notes']['15'] == 'Фінальна нотатка'
            backup['completed'] = [64]
            path.write_text(json.dumps(backup))
            page.locator('#importFile').set_input_files(path)
            page.locator('#importButton').click()
            page.wait_for_function("document.getElementById('backupStatus').textContent.includes('Неправильний')")
            assert page.locator('#progressText').inner_text() == '3 із 64 кроків'
        other = context.new_page()
        other.goto(url)
        other.locator('.module').first.click()
        other.locator('#tasks input').nth(1).check()
        assert 'Імпортований висновок' in other.locator('#moduleNotes').input_value()
        page.wait_for_function("document.getElementById('progressText').textContent==='4 із 64 кроків'")
        page.locator('#courseNav').click()
        page.set_viewport_size({'width': 390, 'height': 844})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert not any('/api/' in r for r in requests)
        assert not errors, errors
        context.close()
        browser.close()
    print('PASS: persistence, export/import, invalid backup rejection, tab sync, mobile, subpath, no API calls')
finally:
    server.shutdown()

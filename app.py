import asyncio
import hashlib
import hmac
import os
import secrets
import sqlite3
import time
import urllib.request
import urllib.parse
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).parent
DB = os.getenv('DATABASE_PATH', str(ROOT / 'learning.sqlite3'))

def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def init():
    with connect() as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, salt TEXT, password TEXT);
        CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id INTEGER, expires REAL);
        CREATE TABLE IF NOT EXISTS progress(user_id INTEGER, lesson INTEGER, PRIMARY KEY(user_id,lesson));
        CREATE TABLE IF NOT EXISTS reminders(user_id INTEGER PRIMARY KEY, chat_id TEXT, hour INTEGER, minute INTEGER, enabled INTEGER, last_sent TEXT DEFAULT '');''')

def password_hash(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 600000).hex()

def user(request):
    with connect() as db:
        row = db.execute('SELECT users.id,username FROM sessions JOIN users ON users.id=sessions.user_id WHERE token=? AND expires>?', (request.cookies.get('session', ''), time.time())).fetchone()
    if row is None:
        raise HTTPException(401, 'Увійдіть у свій обліковий запис')
    return dict(row)

def send_message(chat_id, text):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise RuntimeError('Адміністратор ще не налаштував TELEGRAM_BOT_TOKEN')
    data = urllib.parse.urlencode({'chat_id': chat_id, 'text': text}).encode()
    with urllib.request.urlopen(urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage', data=data), timeout=15) as response:
        import json
        if not json.load(response).get('ok'):
            raise RuntimeError('Telegram не прийняв повідомлення')

async def scheduler():
    while True:
        now = datetime.now(ZoneInfo('Europe/Kyiv'))
        with connect() as db:
            rows = db.execute('SELECT * FROM reminders WHERE enabled=1 AND hour=? AND minute=? AND last_sent<>?', (now.hour, now.minute, now.date().isoformat())).fetchall()
        for row in rows:
            try:
                await asyncio.to_thread(send_message, row['chat_id'], '📚 Час для AI Engineering! Відкрийте навчальний сайт і зробіть наступний крок у своєму проєкті.')
                with connect() as db:
                    db.execute('UPDATE reminders SET last_sent=? WHERE user_id=?', (now.date().isoformat(), row['user_id']))
            except Exception:
                pass  # Do not log URLs containing the bot credential.
        await asyncio.sleep(30)

@asynccontextmanager
async def lifespan(app):
    init()
    task = asyncio.create_task(scheduler())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')

class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=40, pattern=r'^[a-zA-Z0-9_-]+$')
    password: str = Field(min_length=8, max_length=128)

@app.get('/')
def index():
    return FileResponse(ROOT / 'static/index.html')

@app.post('/api/{action}')
def authenticate(action: str, credentials: Credentials):
    if action not in ('login', 'register'):
        raise HTTPException(404)
    with connect() as db:
        if action == 'register':
            salt = secrets.token_hex(16)
            try:
                db.execute('INSERT INTO users(username,salt,password) VALUES(?,?,?)', (credentials.username, salt, password_hash(credentials.password, salt)))
            except sqlite3.IntegrityError:
                raise HTTPException(409, 'Це ім’я вже зайняте')
        row = db.execute('SELECT * FROM users WHERE username=?', (credentials.username,)).fetchone()
        if not row or not hmac.compare_digest(row['password'], password_hash(credentials.password, row['salt'])):
            raise HTTPException(401, 'Неправильне ім’я або пароль')
        token = secrets.token_urlsafe(32)
        db.execute('DELETE FROM sessions WHERE expires<?', (time.time(),))
        db.execute('INSERT INTO sessions VALUES(?,?,?)', (token, row['id'], time.time()+86400*30))
    response = JSONResponse({'username': credentials.username})
    response.set_cookie('session', token, httponly=True, samesite='strict', secure=os.getenv('COOKIE_SECURE') == '1', max_age=86400*30)
    return response

@app.post('/api/session/logout')
def logout(request: Request):
    with connect() as db:
        db.execute('DELETE FROM sessions WHERE token=?', (request.cookies.get('session', ''),))
    response = JSONResponse({'ok': True})
    response.delete_cookie('session')
    return response

@app.get('/api/me')
def me(request: Request):
    current = user(request)
    with connect() as db:
        completed = [r[0] for r in db.execute('SELECT lesson FROM progress WHERE user_id=?', (current['id'],))]
        reminder = db.execute('SELECT chat_id,hour,minute,enabled FROM reminders WHERE user_id=?', (current['id'],)).fetchone()
    return {**current, 'completed': completed, 'reminder': dict(reminder) if reminder else None, 'telegram_available': bool(os.getenv('TELEGRAM_BOT_TOKEN'))}

class Progress(BaseModel):
    completed: bool

@app.put('/api/progress/{lesson}')
def progress(lesson: int, body: Progress, request: Request):
    current = user(request)
    if not 0 <= lesson < 64:
        raise HTTPException(400, 'Невідоме завдання')
    with connect() as db:
        if body.completed:
            db.execute('INSERT OR IGNORE INTO progress VALUES(?,?)', (current['id'], lesson))
        else:
            db.execute('DELETE FROM progress WHERE user_id=? AND lesson=?', (current['id'], lesson))
    return {'ok': True}

class Reminder(BaseModel):
    chat_id: str = Field(pattern=r'^-?[0-9]{1,20}$')
    hour: int = Field(ge=0, le=23)
    minute: int = Field(ge=0, le=59)
    enabled: bool

@app.put('/api/reminder')
def reminder(body: Reminder, request: Request):
    current = user(request)
    with connect() as db:
        db.execute('INSERT INTO reminders(user_id,chat_id,hour,minute,enabled) VALUES(?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET chat_id=excluded.chat_id,hour=excluded.hour,minute=excluded.minute,enabled=excluded.enabled', (current['id'], body.chat_id, body.hour, body.minute, body.enabled))
    return {'ok': True}

@app.post('/api/reminder/test')
async def test_reminder(request: Request):
    current = user(request)
    with connect() as db:
        row = db.execute('SELECT chat_id FROM reminders WHERE user_id=?', (current['id'],)).fetchone()
    if not row:
        raise HTTPException(400, 'Спершу збережіть Chat ID')
    try:
        await asyncio.to_thread(send_message, row['chat_id'], '✅ Нагадування AI Engineering налаштовані!')
    except Exception:
        raise HTTPException(503, 'Не вдалося надіслати: перевірте токен бота, Chat ID та чи натиснули ви /start у боті')
    return {'ok': True}

"""Run: python 12.py. Word-based budget is a toy; use model tokens in lab."""
import sqlite3
import unittest

class Memory:
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE messages(id INTEGER PRIMARY KEY,owner TEXT,session TEXT,role TEXT,text TEXT)')
    def append(self, owner, session, role, text):
        if role not in {'user', 'assistant'}:
            raise ValueError('Role not permitted')
        self.db.execute('INSERT INTO messages(owner,session,role,text) VALUES(?,?,?,?)', (owner, session, role, text))
    def read(self, owner, session):
        return self.db.execute('SELECT role,text FROM messages WHERE owner=? AND session=? ORDER BY id', (owner, session)).fetchall()

def window(messages, budget):
    if budget < 0:
        raise ValueError('Invalid budget')
    selected, used = [], 0
    for message in reversed(messages):
        cost = len(message[1].split())
        if used + cost > budget:
            break
        selected.append(message)
        used += cost
    return list(reversed(selected))

class Tests(unittest.TestCase):
    def test_owner_and_order(self):
        memory = Memory()
        memory.append('A', 'same', 'user', 'first')
        memory.append('B', 'same', 'user', 'private')
        memory.append('A', 'same', 'assistant', 'second')
        self.assertEqual(memory.read('A', 'same'), [('user', 'first'), ('assistant', 'second')])
        with self.assertRaises(ValueError):
            memory.append('A', 'same', 'system', 'override')
        memory.db.close()
    def test_budget(self):
        data = [('user', 'one two'), ('assistant', 'three four')]
        self.assertEqual(window(data, 2), [data[1]])
        self.assertEqual(window(data, 1), [])

if __name__ == '__main__':
    unittest.main()

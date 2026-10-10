"""Run: python 07.py. SQLite lifecycle baseline; not an ANN database."""
import json
import sqlite3
import tempfile
from pathlib import Path
import unittest

class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS chunks(tenant TEXT,id TEXT,text TEXT,vector TEXT,PRIMARY KEY(tenant,id))')
    def upsert(self, tenant, id, text, vector):
        self.db.execute('INSERT INTO chunks VALUES(?,?,?,?) ON CONFLICT(tenant,id) DO UPDATE SET text=excluded.text,vector=excluded.vector', (tenant, id, text, json.dumps(vector)))
        self.db.commit()
    def rows(self, tenant):
        return self.db.execute('SELECT id,text,vector FROM chunks WHERE tenant=? ORDER BY id', (tenant,)).fetchall()
    def delete(self, tenant, id):
        self.db.execute('DELETE FROM chunks WHERE tenant=? AND id=?', (tenant, id))
        self.db.commit()
    def close(self):
        self.db.close()

class Tests(unittest.TestCase):
    def test_lifecycle_and_isolation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / 'index.db')
            store = Store(path)
            store.upsert('A', '1', 'old', [1, 0])
            store.upsert('A', '1', 'new', [0, 1])
            store.upsert('B', '2', 'private', [1, 1])
            store.close()
            store = Store(path)
            self.assertEqual(len(store.rows('A')), 1)
            self.assertEqual(store.rows('A')[0][1], 'new')
            self.assertNotIn('private', str(store.rows('A')))
            store.delete('A', '1')
            self.assertEqual(store.rows('A'), [])
            self.assertEqual(len(store.rows('B')), 1)
            store.close()

if __name__ == '__main__':
    unittest.main()

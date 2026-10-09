import os
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
import app

class Workflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old = app.DB
        app.DB = os.path.join(self.temp.name, 'test.sqlite3')
        self.client = TestClient(app.app)
        self.client.__enter__()
    def tearDown(self):
        self.client.__exit__(None, None, None)
        app.DB = self.old
        self.temp.cleanup()
    def register(self, name):
        return self.client.post('/api/register', json={'username':name, 'password':'password123'})
    def test_persistence_and_isolation(self):
        self.assertEqual(self.client.get('/api/me').status_code, 401)
        self.assertEqual(self.register('alice').status_code, 200)
        self.assertEqual(self.client.put('/api/progress/7',json={'completed':True}).status_code,200)
        self.client.post('/api/session/logout')
        self.assertEqual(self.client.get('/api/me').status_code,401)
        self.register('bob')
        self.assertEqual(self.client.get('/api/me').json()['completed'],[])
        self.client.post('/api/login',json={'username':'alice','password':'password123'})
        self.assertEqual(self.client.get('/api/me').json()['completed'],[7])
        self.assertEqual(self.client.put('/api/progress/64',json={'completed':True}).status_code,400)
        self.client.put('/api/progress/7',json={'completed':False})
        self.assertEqual(self.client.get('/api/me').json()['completed'],[])
    def test_auth_and_reminder(self):
        self.register('alice')
        self.assertEqual(self.register('alice').status_code,409)
        self.assertEqual(self.client.post('/api/login',json={'username':'alice','password':'wrongpass'}).status_code,401)
        self.assertEqual(self.client.put('/api/reminder',json={'chat_id':'12345','hour':19,'minute':0,'enabled':True}).status_code,200)
        self.assertEqual(self.client.get('/api/me').json()['reminder']['hour'],19)
        with patch('app.send_message') as send:
            self.assertEqual(self.client.post('/api/reminder/test').status_code,200)
            self.assertEqual(send.call_args.args[0],'12345')
        with patch('app.send_message',side_effect=RuntimeError('secret')):
            response=self.client.post('/api/reminder/test')
            self.assertEqual(response.status_code,503)
            self.assertNotIn('secret',response.text)
        self.assertEqual(self.client.put('/api/reminder',json={'chat_id':'123','hour':24,'minute':0,'enabled':True}).status_code,422)
    def test_page(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertIn('AI ATELIER',response.text)
        self.assertEqual(self.client.get('/static/course.js').status_code,200)

if __name__=='__main__':
    unittest.main()

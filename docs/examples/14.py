"""Run: python 14.py. Deterministic authorization and input policy."""
import unittest

def validate_question(question, maximum=4000):
    if not isinstance(question, str) or not question.strip() or len(question) > maximum:
        raise ValueError('Invalid question')
    return question.strip()

def authorize_chunks(chunks, authenticated_tenant):
    # authenticated_tenant comes from a verified server session, not question JSON.
    if not authenticated_tenant:
        raise ValueError('Authentication required')
    return [chunk for chunk in chunks if chunk['tenant'] == authenticated_tenant]

def audit_event(request_id, status, duration_ms):
    # Intentionally no question, answer, API key or document content.
    return {'request_id': request_id, 'status': status, 'duration_ms': duration_ms}

class Tests(unittest.TestCase):
    def test_authorization(self):
        rows = [{'tenant': 'A', 'text': 'ok'}, {'tenant': 'B', 'text': 'private'}]
        self.assertEqual(authorize_chunks(rows, 'A'), [rows[0]])
        with self.assertRaises(ValueError):
            authorize_chunks(rows, '')
    def test_input_and_audit(self):
        for question in ['', '  ', 'a'*4001]:
            with self.assertRaises(ValueError):
                validate_question(question)
        event = audit_event('request-1', 'refused', 12)
        self.assertEqual(set(event), {'request_id', 'status', 'duration_ms'})

if __name__ == '__main__':
    unittest.main()

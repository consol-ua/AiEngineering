"""Run: python 08.py. Extractive evidence baseline, not generated RAG."""
import unittest

def chunks(text, source, size=100):
    if size < 1:
        raise ValueError('Positive size required')
    return [{'id': f'{source}:{start}', 'source': source, 'text': text[start:start+size]} for start in range(0, len(text), size)]

def respond(hits):
    if not hits:
        return {'answer': None, 'sources': [], 'refusal_reason': 'no_evidence'}
    return {'answer': '\n'.join(hit['text'] for hit in hits), 'sources': [hit['id'] for hit in hits], 'refusal_reason': None}

def validate_citations(cited_ids, hits):
    allowed = {hit['id'] for hit in hits}
    if not set(cited_ids) <= allowed:
        raise ValueError('Invented citation')
    return True

class Tests(unittest.TestCase):
    def test_evidence(self):
        hits = chunks('RAG додає документи до контексту.', 'guide', 10)
        result = respond(hits)
        self.assertTrue(validate_citations(result['sources'], hits))
        self.assertEqual(hits, chunks('RAG додає документи до контексту.', 'guide', 10))
        self.assertEqual(''.join(h['text'] for h in hits), 'RAG додає документи до контексту.')
    def test_refusal_and_forgery(self):
        self.assertEqual(respond([])['refusal_reason'], 'no_evidence')
        with self.assertRaises(ValueError):
            validate_citations(['invented'], [])

if __name__ == '__main__':
    unittest.main()

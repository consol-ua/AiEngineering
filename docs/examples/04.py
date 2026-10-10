"""Run: python 04.py. Parse/validate only; no inference accuracy claim."""
import json
import unittest

CATEGORIES = {'billing', 'support', 'other'}

def parse_result(raw):
    try:
        value = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError('Invalid JSON') from error
    if not isinstance(value, dict) or set(value) != {'category'}:
        raise ValueError('Expected exactly category')
    if not isinstance(value['category'], str) or value['category'] not in CATEGORIES:
        raise ValueError('Unknown category')
    return value['category']

class Tests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_result('{"category":"support"}'), 'support')
    def test_invalid(self):
        for raw in ['not JSON', '[]', '{}', '{"category":"unknown"}', '{"category":"support","extra":1}', '{"category":[]}']:
            with self.assertRaises(ValueError):
                parse_result(raw)

if __name__ == '__main__':
    unittest.main()

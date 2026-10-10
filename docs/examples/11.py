"""Run: python 11.py. Allowlisted tools, no eval, no external effects."""
import math
import unittest

def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)

def add(args):
    if not isinstance(args, dict) or set(args) != {'a', 'b'} or not all(finite_number(v) for v in args.values()):
        raise ValueError('Require finite a and b')
    result = args['a'] + args['b']
    if not finite_number(result):
        raise ValueError('Result overflow')
    return result

TOOLS = {'add': add}

def dispatch(name, args):
    if name not in TOOLS:
        raise ValueError('Tool not allowed')
    return TOOLS[name](args)

def execute(calls, limit=5):
    if limit < 1 or len(calls) > limit:
        raise ValueError('Step limit exceeded')
    return [dispatch(call['name'], call['args']) for call in calls]

class Tests(unittest.TestCase):
    def test_allowed(self):
        self.assertEqual(execute([{'name': 'add', 'args': {'a': 2, 'b': 3}}]), [5])
    def test_policy(self):
        with self.assertRaises(ValueError):
            dispatch('shell', {})
        for args in [{'a': True, 'b': 1}, {'a': math.nan, 'b': 1}, {'a': 1, 'b': 2, 'extra': 0}]:
            with self.assertRaises(ValueError):
                dispatch('add', args)
        with self.assertRaises(ValueError):
            execute([{}]*6)

if __name__ == '__main__':
    unittest.main()

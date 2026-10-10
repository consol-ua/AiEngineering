"""Run: python 10.py. Retrieval metrics with explicit empty-run failure."""
import unittest

def recall_at_k(expected, retrieved, k):
    if not expected or k < 1:
        raise ValueError('Ground truth and positive k required')
    return len(set(expected) & set(retrieved[:k])) / len(set(expected))

def mrr(cases):
    if not cases:
        raise ValueError('Zero-test evaluation is not valid')
    total = 0.0
    for expected, retrieved in cases:
        if not expected:
            raise ValueError('Ground truth required')
        for rank, id in enumerate(retrieved, 1):
            if id in expected:
                total += 1 / rank
                break
    return total / len(cases)

class Tests(unittest.TestCase):
    def test_known_metrics(self):
        self.assertEqual(recall_at_k(['a', 'b'], ['b', 'x', 'y'], 3), 0.5)
        self.assertEqual(mrr([(['a'], ['a']), (['a'], ['x', 'a']), (['a'], [])]), 0.5)
    def test_empty(self):
        with self.assertRaises(ValueError):
            mrr([])
        with self.assertRaises(ValueError):
            recall_at_k([], ['a'], 1)

if __name__ == '__main__':
    unittest.main()

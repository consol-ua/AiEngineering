"""Run: python 06.py. Toy vectors test ranking; use a real encoder in lab."""
import math
import unittest

def cosine(a, b):
    if not a or len(a) != len(b) or any(not math.isfinite(x) for x in [*a, *b]):
        raise ValueError('Invalid vectors')
    norm = math.sqrt(sum(x*x for x in a)) * math.sqrt(sum(x*x for x in b))
    if not norm:
        raise ValueError('Zero vector')
    return sum(x*y for x, y in zip(a, b)) / norm

def search(query_vector, documents, k=3):
    if not isinstance(k, int) or k < 1:
        raise ValueError('Positive k required')
    scored = [(doc['id'], cosine(query_vector, doc['vector'])) for doc in documents]
    return sorted(scored, key=lambda hit: (-hit[1], hit[0]))[:k]

class Tests(unittest.TestCase):
    def test_rank_and_ties(self):
        docs = [{'id': 'b', 'vector': [1, 0]}, {'id': 'a', 'vector': [1, 0]}, {'id': 'c', 'vector': [0, 1]}]
        self.assertEqual([x[0] for x in search([1, 0], docs, 2)], ['a', 'b'])
    def test_dimensions(self):
        with self.assertRaises(ValueError):
            search([1], [{'id': 'a', 'vector': [1, 0]}])
        with self.assertRaises(ValueError):
            search([0], [{'id': 'a', 'vector': [1]}])

if __name__ == '__main__':
    unittest.main()

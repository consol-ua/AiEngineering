"""Run: python 02.py. Standard-library cosine baseline."""
import math
import unittest

def cosine(a, b):
    if not a or len(a) != len(b):
        raise ValueError('Equal nonempty dimensions required')
    if any(not math.isfinite(x) for x in [*a, *b]):
        raise ValueError('Finite coordinates required')
    norm_a = math.sqrt(math.fsum(x*x for x in a))
    norm_b = math.sqrt(math.fsum(x*x for x in b))
    if norm_a == 0 or norm_b == 0:
        raise ValueError('Zero vector')
    return math.fsum(x*y for x, y in zip(a, b)) / norm_a / norm_b

class Tests(unittest.TestCase):
    def test_geometry(self):
        self.assertAlmostEqual(cosine([1, 0], [1, 0]), 1)
        self.assertAlmostEqual(cosine([1, 0], [0, 1]), 0)
        self.assertAlmostEqual(cosine([1, 0], [1, 1]), 1/math.sqrt(2))
        self.assertAlmostEqual(cosine([1, 1], [2, 2]), 1)
    def test_bad_vectors(self):
        for a, b in [([], []), ([1], [1, 2]), ([0], [1]), ([math.nan], [1]), ([math.inf], [1])]:
            with self.assertRaises(ValueError):
                cosine(a, b)

if __name__ == '__main__':
    unittest.main()

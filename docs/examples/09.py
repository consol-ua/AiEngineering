"""Run: python 09.py. Character splitter and rank fusion baseline."""
import unittest

def split(text, size=100, overlap=20):
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError('Require 0 <= overlap < size')
    output = []
    start = 0
    while start < len(text):
        output.append(text[start:start+size])
        if start + size >= len(text):
            break
        start += size - overlap
    return output

def rrf(lists, c=60):
    if c < 0:
        raise ValueError('Nonnegative smoothing required')
    scores = {}
    for ranking in lists:
        seen = set()
        for rank, id in enumerate(ranking, 1):
            if id in seen:
                raise ValueError('Duplicate ID in ranking')
            seen.add(id)
            scores[id] = scores.get(id, 0) + 1 / (c + rank)
    return sorted(scores.items(), key=lambda x: (-x[1], x[0]))

class Tests(unittest.TestCase):
    def test_coverage(self):
        self.assertEqual(split('abcdefgh', 4, 1), ['abcd', 'defg', 'gh'])
        with self.assertRaises(ValueError):
            split('abc', 4, 4)
    def test_fusion(self):
        result = rrf([['a', 'b'], ['b', 'c']])
        self.assertEqual(result[0][0], 'b')
        self.assertEqual(len(result), 3)
        with self.assertRaises(ValueError):
            rrf([['a', 'a']])

if __name__ == '__main__':
    unittest.main()

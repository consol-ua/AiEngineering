"""Run: python 03.py. Toy logits; this is not an LLM/tokenizer."""
import math
import unittest

def softmax(logits, temperature=1.0):
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError('Positive finite temperature required')
    if not logits or any(not math.isfinite(x) for x in logits):
        raise ValueError('Finite nonempty logits required')
    maximum = max(logits)
    weights = [math.exp((x - maximum) / temperature) for x in logits]
    total = math.fsum(weights)
    return [x / total for x in weights]

class Tests(unittest.TestCase):
    def test_distribution(self):
        values = softmax([1000, 999])
        self.assertAlmostEqual(sum(values), 1)
        self.assertAlmostEqual(values[0], 0.7310585786)
        self.assertGreater(softmax([2, 1], 0.5)[0], softmax([2, 1], 1)[0])
    def test_invalid(self):
        for logits, temperature in [([], 1), ([1], 0), ([1], -1), ([math.nan], 1), ([1], math.inf)]:
            with self.assertRaises(ValueError):
                softmax(logits, temperature)

if __name__ == '__main__':
    unittest.main()

"""Run: python 13.py. Lower bound only, not full memory requirement."""
import math
import unittest

def weight_bytes(parameters, bits):
    if type(parameters) is not int or parameters <= 0 or type(bits) is not int or bits <= 0:
        raise ValueError('Positive integer parameters and bits required')
    return math.ceil(parameters * bits / 8)

def sizing(parameters, bits, available_bytes):
    weights = weight_bytes(parameters, bits)
    return {'weight_lower_bound': weights, 'available': available_bytes,
            'weights_fit': weights <= available_bytes,
            'runtime_readiness': 'unverified: KV, activations and runtime not measured'}

class Tests(unittest.TestCase):
    def test_lower_bound(self):
        self.assertEqual(weight_bytes(1_000_000_000, 4), 500_000_000)
        self.assertEqual(weight_bytes(1_000_000_000, 16), 2_000_000_000)
        self.assertIn('unverified', sizing(1000, 4, 10000)['runtime_readiness'])
    def test_invalid(self):
        for parameters, bits in [(0, 4), (-1, 4), (10, 0), (True, 4)]:
            with self.assertRaises(ValueError):
                weight_bytes(parameters, bits)

if __name__ == '__main__':
    unittest.main()

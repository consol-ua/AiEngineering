"""Run: python 15.py. Nearest-rank percentiles, failures remain visible."""
import math
import unittest

def percentile(values, p):
    if not values or not 0 < p <= 1 or any(not math.isfinite(x) or x < 0 for x in values):
        raise ValueError('Valid samples and percentile required')
    ordered = sorted(values)
    return ordered[math.ceil(p*len(ordered))-1]

def report(success_latencies, failures):
    if type(failures) is not int or failures < 0:
        raise ValueError('Invalid failures')
    total = len(success_latencies) + failures
    if not total:
        raise ValueError('No requests executed')
    return {'total': total, 'failures': failures,
            'completion_rate': len(success_latencies)/total,
            'p95_success_only': percentile(success_latencies, 0.95) if success_latencies else None}

class Tests(unittest.TestCase):
    def test_percentile(self):
        self.assertEqual(percentile(list(range(1, 21)), 0.95), 19)
        self.assertEqual(percentile([3], 0.5), 3)
    def test_failure_accounting(self):
        self.assertEqual(report([1, 2], 2)['completion_rate'], 0.5)
        self.assertIsNone(report([], 3)['p95_success_only'])
        with self.assertRaises(ValueError):
            report([], 0)
        with self.assertRaises(ValueError):
            percentile([], 0.95)

if __name__ == '__main__':
    unittest.main()

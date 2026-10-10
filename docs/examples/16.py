"""Run: python 16.py. Illustrative thresholds, not production policy."""
import math
import unittest

POLICY = {'min_questions': 30, 'min_recall': 0.8, 'max_p95_ms': 5000}

def release_gate(report):
    reasons = []
    for key in ['questions', 'recall_at_3', 'p95_ms', 'tenant_leaks', 'clean_start_verified']:
        if key not in report:
            reasons.append('Missing: ' + key)
    if reasons:
        return {'ready': False, 'reasons': reasons}
    for key in ['questions', 'recall_at_3', 'p95_ms', 'tenant_leaks']:
        if type(report[key]) not in (int, float) or not math.isfinite(report[key]) or report[key] < 0:
            reasons.append('Invalid metric: ' + key)
    if reasons:
        return {'ready': False, 'reasons': reasons}
    if report['questions'] < POLICY['min_questions']:
        reasons.append('Insufficient evaluation questions')
    if not POLICY['min_recall'] <= report['recall_at_3'] <= 1:
        reasons.append('Retrieval quality gate failed')
    if report['p95_ms'] > POLICY['max_p95_ms']:
        reasons.append('Latency gate failed')
    if report['tenant_leaks'] != 0:
        reasons.append('Critical tenant leak')
    if report['clean_start_verified'] is not True:
        reasons.append('Clean start unverified')
    return {'ready': not reasons, 'reasons': reasons}

class Tests(unittest.TestCase):
    def test_ready(self):
        self.assertTrue(release_gate({'questions': 30, 'recall_at_3': 0.9, 'p95_ms': 1000, 'tenant_leaks': 0, 'clean_start_verified': True})['ready'])
    def test_missing_and_critical(self):
        self.assertFalse(release_gate({})['ready'])
        value = {'questions': 30, 'recall_at_3': 0.99, 'p95_ms': 10, 'tenant_leaks': 1, 'clean_start_verified': True}
        self.assertIn('Critical tenant leak', release_gate(value)['reasons'])
        value['tenant_leaks'] = 0
        value['p95_ms'] = math.nan
        self.assertFalse(release_gate(value)['ready'])

if __name__ == '__main__':
    unittest.main()

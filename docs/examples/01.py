"""Run: python 01.py. Fake provider tests the contract, not LLM quality."""
from dataclasses import dataclass
from typing import Protocol
import unittest

class Provider(Protocol):
    def generate(self, question: str) -> str: ...

@dataclass(frozen=True)
class Answer:
    status: str
    answer: str

class FakeProvider:
    def generate(self, question):
        return 'Відповідь baseline: ' + question

def ask(question: str, provider: Provider) -> Answer:
    if not isinstance(question, str) or not question.strip():
        raise ValueError('Question is required')
    if len(question) > 4000:
        raise ValueError('Question is too long')
    answer = provider.generate(question.strip())
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError('Invalid provider response')
    return Answer('ok', answer)

class Tests(unittest.TestCase):
    def test_contract(self):
        result = ask('Що таке RAG?', FakeProvider())
        self.assertEqual(result.status, 'ok')
        self.assertIn('RAG', result.answer)
    def test_reject_before_provider(self):
        class Never:
            def generate(self, question):
                raise AssertionError('Must not be called')
        for value in ['', '   ', None, 'a' * 4001]:
            with self.assertRaises(ValueError):
                ask(value, Never())

if __name__ == '__main__':
    unittest.main()

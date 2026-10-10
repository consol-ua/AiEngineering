"""Run: python 05.py. Bounded attempt retries with a fake async provider.
A real HTTP adapter must also enforce the overall request deadline.
"""
import asyncio
import unittest

class TransientError(Exception):
    pass

async def generate(provider, question, attempts=2, timeout=0.1, backoff=0.01):
    if attempts < 1 or timeout <= 0 or backoff < 0:
        raise ValueError('Invalid retry policy')
    for attempt in range(attempts):
        try:
            return await asyncio.wait_for(provider(question), timeout)
        except (TransientError, asyncio.TimeoutError) as error:
            if attempt + 1 == attempts:
                raise TransientError('Provider unavailable') from error
            await asyncio.sleep(backoff * 2**attempt)

class Tests(unittest.IsolatedAsyncioTestCase):
    async def test_retry_then_success(self):
        calls = 0
        async def fake(question):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise TransientError('503')
            return 'ok'
        self.assertEqual(await generate(fake, 'q'), 'ok')
        self.assertEqual(calls, 2)
    async def test_permanent_not_retried(self):
        calls = 0
        async def fake(question):
            nonlocal calls
            calls += 1
            raise ValueError('Invalid request')
        with self.assertRaises(ValueError):
            await generate(fake, 'q')
        self.assertEqual(calls, 1)
    async def test_timeout(self):
        async def slow(question):
            await asyncio.sleep(1)
        with self.assertRaises(TransientError):
            await generate(slow, 'q', attempts=1, timeout=0.01)

if __name__ == '__main__':
    unittest.main()

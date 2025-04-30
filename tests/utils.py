import asyncio
from contextvars import ContextVar
import time


contextvar_counter = ContextVar("contextvar_counter", default=0)


class Counter:
    def __init__(self):
        self.counter = 0

    def reset_counters(self):
        self.counter = 0

    def increment(self):
        self.counter += 1

    def count_to_n(self, n):
        self.reset_counters()
        for _ in range(n):
            self.increment()
            time.sleep(0)

        return self.counter


class ContextVarCounter(Counter):
    @property
    def counter(self):
        return contextvar_counter.get()
    
    @counter.setter
    def counter(self, value):
        contextvar_counter.set(value)


class CounterAsync(Counter):
    async def count_to_n(self, n):
        self.reset_counters()
        for _ in range(n):
            self.increment()
            await asyncio.sleep(0)

        return self.counter


class ContextVarCounterAsync(CounterAsync, ContextVarCounter):
    pass


def parse_results(results, print_debug=False):
    """
    note: low active thread count may give false positive
            e.g. there is no context switching if only one thread is active
    """
    is_thread_safe = True
    for result in results:
        if not result['durations']:
            print(f"worker_id {result['worker_id']:03d} didn't process any inputs")
            continue

        if result['validity_checks'] and all(i is not None for i in result['validity_checks']):
            result['correct_results'] = result['validity_checks'].count(True)
            result['incorrect_results'] = result['validity_checks'].count(False)
            result['is_thread_safe'] = all(result['validity_checks'])            
            is_thread_safe = is_thread_safe and result['is_thread_safe']
     
        if print_debug:
            print(f"\n{'='*80}")
            print(f"worker_id {result['worker_id']:03d}")
            print(f"Validity Checks: {result['validity_checks']}")
            print(f"correct results: {result['correct_results']}")
            print(f"incorrect results: {result['incorrect_results']}")

    return results, is_thread_safe
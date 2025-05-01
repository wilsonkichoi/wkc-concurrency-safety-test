# wkc-concurrency-safety-test

Simple Python script to test if the give funciton is thread/coroutine safe

Depends on how your program works, this may not be able to just plug and play. But it is simple enough that you should be able to adapt it to run with your program.
Two main modules are
- src/wkc_concurrency_safety_test/coroutine_runner.py
- src/wkc_concurrency_safety_test/thread_runner.py

### TODO
- add doc string

### usage example
```
import time
from wkc_concurrency_safety_test import thread_runner


############################################################
# non thread safe example
############################################################

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


counter = Counter()
test_data = [{ 
                'args': [10000],
                'kwargs': {},
                'expected_output': 10000,
            }]
results = thread_runner.run(counter.count_to_n, test_data, thread_count=9, test_size=77, print_debug=True)
is_thread_safe = all([all(result['validity_checks']) for result in results])



############################################################
# thread safe example
############################################################

from contextvars import ContextVar
contextvar_counter = ContextVar("contextvar_counter", default=0)

class ContextVarCounter(Counter):
    @property
    def counter(self):
        return contextvar_counter.get()
    
    @counter.setter
    def counter(self, value):
        contextvar_counter.set(value)

contextvar_conter = ContextVarCounter()
test_data = [{ 
                'args': [10000],
                'kwargs': {},
                'expected_output': 10000,
            }]
results = thread_runner.run(contextvar_conter.count_to_n, test_data, thread_count=9, test_size=77, print_debug=True)
is_thread_safe = all([all(result['validity_checks']) for result in results])
```

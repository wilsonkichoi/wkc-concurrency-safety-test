# wkc-concurrency-safety-test

Simple Python script to test if the give funciton is thread/coroutine safe

Depends on how your program works, this may not be able to just plug and play. But it is simple enough that you should be able to adapt it to run with your program.
Two main modules are
- src/wkc_concurrency_safety_test/coroutine_runner.py
- src/wkc_concurrency_safety_test/thread_runner.py

### TODO
- add doc string

### usage example

#### import thread_runner
```
from wkc_concurrency_safety_test import thread_runner
```

#### non thread safe counter
```
import time 

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
            time.sleep(0) # force context switch

        return self.counter

```

#### use thread_runner to test the counter

the run funciton take the follow arguments
- func (callable): function to be tested
- test_data (list[dict]): test data (see test_data format below)
- thread_count (int): number of threads to use for testing
- test_size (int): number of tests to run. test data will be shuffled and inflated (shrinked) to test_size.
- print_debug (bool): whether to print debug messages


#### test_data format
```
[
    {
        'args': [args], # for the func
        'kwargs': {kwargs}, # for the func
        'expected_output': expected_output # (optional if validation_func is provided)
        'validation_func': lambda x: x['output'] == expected_output, # (optional if expected_output is provided)
    },
    ...
]
```

#### run test
```
counter = Counter()
test_data = [{ 
                'args': [10000],
                'kwargs': {},
                'expected_output': 10000,
            }]
results = thread_runner.run(counter.count_to_n, test_data, thread_count=9, test_size=77, print_debug=True)
is_thread_safe = all([all(result['validity_checks']) for result in results])
```

#### test thread safe counter
```
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

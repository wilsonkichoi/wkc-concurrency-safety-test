import asyncio

from .thread_runner import run as thread_run
from .coroutine_runner import run as coroutine_run


DEFAULT_WORKER_COUNT = 100
DEFAULT_TEST_SIZE = 1000

def call_runner_by_excution_model(func,
                                  test_data: list,
                                  worker_count:int = DEFAULT_WORKER_COUNT,
                                  test_size:int = DEFAULT_TEST_SIZE,
                                  excution_model:str = 'thread', # "thread" or "async"
                                  print_debug:bool = False):
    if excution_model == "thread":                   
        results = thread_run(func, test_data, worker_count, test_size, print_debug)
    elif excution_model == "async":
        print("wilson")
        results = asyncio.run(coroutine_run(func, test_data, worker_count, test_size, print_debug))

    return results

import queue
import threading
import time

from .utils import inflate_and_shuffle


class Runner(threading.Thread):
    def __init__(self, worker_id, func, event, input_queue, print_debug=False):
        super().__init__()
        self.worker_id = worker_id
        self.func = func
        self.event = event
        self.input_queue = input_queue
        self.print_debug = print_debug
        
        self.result = {
            'inputs': [],
            'outputs': [],
            'durations': [],
            'expected_outputs': [],
            'validation_funcs': [],
            'validity_checks': [],
        }

    def run(self):
        while not self.event.is_set():
            time.sleep(0.001)
            print(f"\nworker_id {self.worker_id:03d} waiting...")

        try:
            input = self.input_queue.get(timeout=1)
            while input:
                # print progress
                if len(self.result['durations']) % 100 == 0 and self.print_debug:
                    print(".", end="", flush=True)

                # run function 
                start_time = time.thread_time()
                output = self.func(*input['args'], **input['kwargs'])
                end_time = time.thread_time()

                # check validity (optional)
                expected_output = input.get('expected_output')
                validation_func = input.get('validation_func')
                if expected_output:
                    validity_check = expected_output == output
                elif validation_func:
                    validity_check = validation_func(output)
                else:
                    validity_check = None

                # store results
                self.result['inputs'].append(input)
                self.result['outputs'].append(output)
                self.result['durations'].append(end_time - start_time)
                self.result['expected_outputs'].append(expected_output)
                self.result['validation_funcs'].append(validation_func)
                self.result['validity_checks'].append(validity_check)

                # get next
                input = self.input_queue.get(timeout=1)
        except queue.Empty as ex:
            if self.print_debug:
                print(f"worker_id {self.worker_id:03d} finished, {len(self.result['durations'])} processed")
        except Exception as ex:
            print(ex)

def run(func,
        test_data: list[dict],
        thread_count:int,
        test_size:int,
        print_debug:bool = False):
    """
    Parameters:
        func (callable): function to be tested
        test_data (list[dict]): test data (see test_data format below)
        thread_count (int): number of threads to use for testing
        test_size (int): number of tests to run. test data will be shuffled and inflated (shrinked) to test_size.
        print_debug (bool): whether to print debug messages

    test_data format:
    [
        {
            'args': [args], # for the func
            'kwargs': {kwargs}, # for the func
            'expected_result': expected_result # (optional) 
            'expected_output': lambda x: x['output'] == expected_output, # (optional)
        },
        ...
    ]
    """
    event = threading.Event()
    input_queue = queue.Queue()

    shuffled_test_data = inflate_and_shuffle(test_data, test_size)
    for i in shuffled_test_data:
        input_queue.put(i)

    threads = []
    for i in range(1, thread_count + 1):
        t = Runner(i, func, event, input_queue, print_debug)
        t.start()
        threads.append(t)

    time.sleep(0.1)

    event.set()
    for t in threads:
        t.join()

    # generate results
    results = []
    for t in threads:
        results.append({
            'worker_id': t.worker_id,
            'durations': t.result['durations'],
            'inputs': t.result['inputs'],
            'outputs': t.result['outputs'],
            'expected_outputs': t.result['expected_outputs'],
            'validation_funcs': t.result['validation_funcs'],
            'validity_checks': t.result['validity_checks'],
        })

    return results

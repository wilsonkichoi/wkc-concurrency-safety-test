import asyncio
import time

from .utils import inflate_and_shuffle


async def runner(worker_id, func, event, input_queue, print_debug=False):
    while not event.is_set():
        await asyncio.sleep(0.001)
        print(f"\nworker_id {worker_id:03d} waiting...")

    result = {
        'worker_id': worker_id,
        'durations': [],
        'inputs': [],
        'outputs': [],
        'expected_outputs': [],
        'validation_funcs': [],
        'validity_checks': [],
    }

    while not input_queue.empty():
        # print progress
        if len(result['durations']) % 100 == 0 and print_debug:
            print(".", end="", flush=True)

        try:
            # get input
            input = input_queue.get_nowait()

            # run function
            start_time = time.thread_time()
            output = await func(*input['args'], **input['kwargs'])
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
            result['inputs'].append(input)
            result['outputs'].append(output)
            result['durations'].append(end_time - start_time)
            result['expected_outputs'].append(expected_output)
            result['validation_funcs'].append(validation_func)
            result['validity_checks'].append(validity_check)
            
            input_queue.task_done()
        except asyncio.QueueEmpty:
            if print_debug:
                print(f"worker_id {worker_id:03d} finished, {len(result['durations'])} processed")
        except Exception as ex:
            print(ex)

    return result


async def run(func,
              test_data: list[dict],
              task_count:int,
              test_size:int,
              print_debug:bool = False):
    """
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
    event = asyncio.Event()
    input_queue = asyncio.Queue()

    shuffled_test_data = inflate_and_shuffle(test_data, test_size)
    for i in shuffled_test_data:
        input_queue.put_nowait(i)

    tasks = []
    for i in range(1, task_count + 1):
        task = asyncio.create_task(runner(i, func, event, input_queue, print_debug))
        tasks.append(task)

    await asyncio.sleep(0.1)

    event.set()
    await input_queue.join()

    results = await asyncio.gather(*tasks)
    return results

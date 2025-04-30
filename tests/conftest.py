import pytest

from .utils import Counter, ContextVarCounter, CounterAsync, ContextVarCounterAsync

@pytest.fixture(params=[
    pytest.param({'class': Counter, 'excution_model': 'thread', 'is_thread_safe': False}, id='Counter'),
    pytest.param({'class': ContextVarCounter, 'excution_model': 'thread', 'is_thread_safe': True}, id='ContextVarCounter'),
    pytest.param({'class': CounterAsync, 'excution_model': 'async', 'is_thread_safe': False}, id='CounterAsync'),
    pytest.param({'class': ContextVarCounterAsync, 'excution_model': 'async', 'is_thread_safe': True}, id='ContextVarCounterAsync'),
])
def config(request):
    counter = request.param['class']()
    n = 10000
    return {
        'class': request.param['class'],
        'counter': counter, 
        'is_thread_safe': request.param['is_thread_safe'],
        'runner_args': {
            'func': counter.count_to_n,
            'test_data': [{
                'args': [n],
                'kwargs': {},
                'expected_output': n,
            }],
            'worker_count': 9,
            'test_size': 77,
            'excution_model': request.param['excution_model'],
            'print_debug': True,
        },
    }

@pytest.fixture()
def test_validation_func_config(config):
    n = 1000
    config['runner_args']['test_data'] = [{
        'args': [1000],
        'kwargs': {},
        'validation_func': lambda x: x == 1000,
    }]
    config['runner_args']['worker_count'] = 3
    config['runner_args']['test_size'] = 5
    return config

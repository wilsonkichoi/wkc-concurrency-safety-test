from wkc_concurrency_safety_test.main import call_runner_by_excution_model
from ..utils import parse_results


def test_concurrency_safety(config):
    results = call_runner_by_excution_model(**config['runner_args'])
    results, is_thread_safe = parse_results(results)
    assert is_thread_safe == config['is_thread_safe']


def test_concurrency_safety_with_validation_func(test_validation_func_config):
    results = call_runner_by_excution_model(**test_validation_func_config['runner_args'])
    results, is_thread_safe = parse_results(results)
    assert is_thread_safe == test_validation_func_config['is_thread_safe']

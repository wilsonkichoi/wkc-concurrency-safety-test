clean:
	rm -rf dist build src/wkc_concurrency_safety_test.egg-info

build: clean
	python -m build

install: uninstall
	pip install dist/wkc_concurrency_safety_test-0.0.1-py3-none-any.whl

uninstall:
	pip uninstall -y wkc-concurrency-safety-test

install-dev: uninstall clean
	pip install -e ".[dev]"

test:
	pytest -v --cov=wkc_concurrency_safety_test --cov-branch --cov-report=term-missing

test-debug:
	pytest -s --pdb

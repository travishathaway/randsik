.PHONY: help clean clean-pyc clean-build list test test-all coverage docs release sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	poetry run flake8 --max-line-length 99 randsik test

test:
	poetry run pytest

coverage:
	poetry run coverage run --source randsik -m pytest
	poetry run coverage report -m
	poetry run coverage html

docs:
	rm -f docs/randsik.rst
	rm -f docs/modules.rst
	poetry run sphinx-apidoc -o docs/ randsik
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

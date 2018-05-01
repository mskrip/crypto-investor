.PHONY: install lint venv test

all: install lint

venv:
	python3 -m venv .venv/

install:
	pip install --upgrade setuptools
	pip install -e .[test]

lint:
	flake8

test:
	python3 -m pytest

sdist:
	python3 setup.py sdist

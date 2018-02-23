.PHONY: install lint venv test

all: install lint

venv:
	python -m venv .venv/

install:
	pip install --upgrade setuptools
	pip install -e .[test]

lint:
	flake8

test:
	python -m unittest

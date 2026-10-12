.PHONY: install demos test
install:
	pip install -r requirements.txt pytest
demos:
	@for f in implementations/*/*.py benchmark/run.py; do echo "\n=== $$f"; python $$f; done
test:
	pytest -q

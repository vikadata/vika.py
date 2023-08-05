

.PHONY: install
install:
	poetry install


.PHONY: test
test:
	poetry run pytest
#poetry run python -m unittest


	
.PHONY: setup
setup:
	poetry run python setup.py sdist bdist_wheel
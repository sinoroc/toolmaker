#


source_dir := ./src
tests_dir := ./test


.DEFAULT_GOAL := develop


.PHONY: develop
develop:
	python3 setup.py develop


.PHONY: package
package: sdist wheel check zapp


.PHONY: sdist
sdist:
	python3 setup.py sdist


.PHONY: wheel
wheel:
	python3 setup.py bdist_wheel


.PHONY: zapp
zapp:
	python3 setup.py bdist_zapp


.PHONY: check
check: sdist wheel
	python3 -m twine check dist/*.tar.gz
	python3 -m twine check dist/*.whl


.PHONY: lint
lint:
	python3 -m pytest --pep8 --pylint -m 'pep8 or pylint'


.PHONY: pep8
pep8:
	python3 -m pytest --pep8 -m pep8


.PHONY: pylint
pylint:
	python3 -m pytest --pylint -m pylint


.PHONY: test
test: pytest


.PHONY: pytest
pytest:
	python3 -m pytest


.PHONY: review
review:
	python3 -m pytest --pep8 --pylint


.PHONY: clean
clean:
	$(RM) --recursive ./.eggs/
	$(RM) --recursive ./.pytest_cache/
	$(RM) --recursive ./build/
	$(RM) --recursive ./dist/
	$(RM) --recursive ./__pycache__/
	find $(source_dir) -name '*.dist-info' -type d -exec $(RM) --recursive {} +
	find $(source_dir) -name '*.egg-info' -type d -exec $(RM) --recursive {} +
	find $(source_dir) -name '*.pyc' -type f -exec $(RM) {} +
	find $(tests_dir) -name '*.pyc' -type f -exec $(RM) {} +
	find $(source_dir) -name '__pycache__' -type d -exec $(RM) --recursive {} +
	find $(tests_dir) -name '__pycache__' -type d -exec $(RM) --recursive {} +


#
# Options
#

# Disable default rules and suffixes (improve speed and avoid unexpected behaviour)
MAKEFLAGS := --no-builtin-rules
.SUFFIXES:


# EOF

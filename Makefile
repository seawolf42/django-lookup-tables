# -------------------------------------
# MAKEFILE
# -------------------------------------


#
# environment
#

ifndef VIRTUAL_ENV
$(error VIRTUAL_ENV is not set)
endif


#
# commands for artifact cleanup
#

PHONY: clean.build
clean.build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

PHONY: clean.pyc
clean.pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete

PHONY: clean
clean: clean.build clean.pyc


#
# commands for testing
#

PHONY: test.flake8
test.flake8:
	flake8 .

PHONY: test.unittests
test.unittests:
	PYTHONPATH=${PYTHONPATH} python runtests.py tests

PHONY: test
test: test.unittests test.flake8


#
# commands for packaging and deploying to pypi
#

PHONY: docs
docs:
	pandoc -o README.rst README.md

PHONY: sdist
sdist: docs
	python setup.py sdist

PHONY: release
release: clean sdist
	python setup.py sdist upload
	python setup.py bdist_wheel upload

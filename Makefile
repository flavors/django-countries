.DEFAULT_GOAL=test

test:
	@pytest\
		--verbose\
		--fail-on-template-vars\
		--cov=countries_flavor\
		--cov-config .coveragerc\
		--cov-report term\
		--cov-report xml

test-all:
	@tox

release:
	@python setup.py sdist upload
	@python setup.py bdist_wheel upload

.PHONY: test test-all release

.ONESHELL:

PROJECT_NAME=cp4_ai

PKG_NAME=$(PROJECT_NAME)

HOST=rpi-p4
REMOTE_PATH=

VERSION=$(shell grep version= setup.py | cut -d= -f2 | cut -d\' -f 2)

default: build

.PHONY: init
init:
	pip install -r requirements-dev.txt

.PHONY: test
test:
	PYTHONPATH=. pytest tests

.PHONY: lint
lint:
	mypy $(PROJECT_NAME)

.PHONY: build
build:
	@mkdir -p dist/arch
	if test -f dist/*.whl ; then mv dist/*.whl dist/arch ; fi
	python3 setup.py bdist_wheel

.PHONY: deploy
deploy:
	ssh $(HOST) 'rm $(PROJECT_NAME)-*-py3-none-any.whl'
	scp dist/*.whl $(HOST):$(REMOTE_PATH)
	ssh $(HOST) 'pip install $(PKG_NAME)-$(VERSION)-py3-none-any.whl --force-reinstall --no-deps --no-warn-script-location'

.PHONY: restart
restart:
	ssh $(HOST) 'sudo systemctl restart cp4-ai'

.PHONY: update-config
update-config:
	scp systemd/cp4-ai.service $(HOST):$(REMOTE_PATH)

.PHONY: show-version
show-version:
	@echo $(VERSION)

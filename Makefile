VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
CONTAINER_NAME = discord-it-trivia
CONTAINER_PROD_TAG = latest

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

install-dev: venv
	$(PIP) install -r requirements-dev.txt
	pre-commit install

build:
	docker build -t chrisjhart/$(CONTAINER_NAME):latest .

run:
	docker run --rm --name $(CONTAINER_NAME) chrisjhart/$(CONTAINER_NAME):latest

run-dev: build
	docker run --rm --name $(CONTAINER_NAME)-dev -v $(PWD)/.env:/app/.env -e DEBUG=true chrisjhart/$(CONTAINER_NAME):latest
	docker logs -f $(CONTAINER_NAME)-dev

run-debug:
	docker run --rm --name $(CONTAINER_NAME) chrisjhart/$(CONTAINER_NAME):latest -c "pip install debugpy -t /tmp && python /tmp/debugpy --wait-for-client --listen 0.0.0.0:5678 ./main.py

test: venv
	python -m pytest tests/

clean:
	rm -rf venv

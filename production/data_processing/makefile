VERSION=0.1.0
LAMBDA_NAME = jospin_data_processing
MAIN_FILE=data_processing.py
PYTHON=.venv-$(LAMBDA_NAME)/bin/python3
PIP=.venv-$(LAMBDA_NAME)/bin/pip

venv:
	python3 -m venv .venv-$(LAMBDA_NAME);

setup:
	$(PIP) install -r requirements.txt;

run:
	$(PYTHON) ./src/$(MAIN_FILE)

deploy:

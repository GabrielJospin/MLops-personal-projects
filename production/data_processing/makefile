VERSION=0.1.0
LAMBDA_NAME = jospin_data_processing
S3_BUCKET = jospin-gabriel-mlops-projects
DIST_FILE=data-processing-$(VERSION).zip
MAIN_FILE=data_processing.py
PYTHON=.venv-$(LAMBDA_NAME)/bin/python3
PIP=.venv-$(LAMBDA_NAME)/bin/pip

venv:
	python3 -m venv .venv-$(LAMBDA_NAME);

setup:
	$(PIP) install -r requirements.txt;

run:
	$(PYTHON) ./src/$(MAIN_FILE)

clean:
	rm -r build || true
	rm -r dist || true

build: clean
	mkdir build
	cp requirements.txt build/
	cp -R src/* build/
	cd build && ../$(PIP) install --no-cache-dir --no-deps -r requirements.txt --force -t .
	mkdir dist
	cd build && zip -ur ../dist/$(DIST_FILE) * -x "bin/*" requirements.txt setup.cfg


deploy:
	aws s3 cp dist/$(DIST_FILE) s3://$(S3_BUCKET)/src/lambda/$(LAMBDA_NAME)/dist/$(DIST_FILE)
	aws lambda update-function-code \
		--function-name $(LAMBDA_NAME) \
		--s3-bucket $(S3_BUCKET) \
		--s3-key src/lambda/$(LAMBDA_NAME)/dist/$(DIST_FILE)

full_deploy: build deploy
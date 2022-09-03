install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

unit-tests:
	python -m pytest -vv --cov

integration-tests:
	bash src/integration-tests/run_tests.sh

tests: unit-tests integration-tests

inference-infra:
	python src/inference_infra/create_inferinfra.py

training-pipeline:
	python src/training/training_pipeline.py

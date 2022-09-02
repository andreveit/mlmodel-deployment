install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov


inference-infra:
	python src/inference_infra/create_inferinfra.py


training-pipeline:
	python src/training/training_pipeline.py

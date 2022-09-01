install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov


training-pipeline:
	python src/training/training_pipeline.py


.PHONY : pypi-ingest format

pypi-ingest:
	poetry run python -m ingestion.pipeline

format:
	ruff format .

test:
	pytest tests
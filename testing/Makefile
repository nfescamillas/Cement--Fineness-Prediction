test:
	pytest tests/

integration-test:test
	bash integration_test/run.sh

quality_checks: integration-test
	isort .
	black .
	pylint --recursive=y . 

setup: 
	pipenv install --dev
	pre-commit install 

	
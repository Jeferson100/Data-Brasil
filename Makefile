install:
	# Comando para atualizar pip e instalar dependências do arquivo requirements.txt
	# pip install --user -r requirements.txt
	pip install --upgrade pip && \
	pip install -r requirements.txt

format:
	black brazilian_data/*.py tests/*.py

lint:
	pylint --disable=R,C brazilian_data/*.py tests/*.py

test:
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: install lint format test
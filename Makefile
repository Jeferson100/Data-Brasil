install:
	# Comando para atualizar pip e instalar dependências do arquivo requirements.txt
	# pip install --user -r requirements.txt
	pip install --upgrade pip && \
	pip install -r requirements.txt

uv_install:
	pip install uv && \
	uv pip install --upgrade pip && \
		uv pip install -r requirements.txt

format:
	black brazilian_data/*.py tests/*.py

lint:
	pylint --disable=R,C brazilian_data/*.py tests/*.py

ruff_lint:
	ruff check brazilian_data/*.py

pyright:
	pyright brazilian_data/*.py

ruff_format:
	ruff format brazilian_data/*.py

typemypy:
	typemypy brazilian_data/*.py

test:
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: uv_install lint ruff_lint format ruff_format pyright typemypy test
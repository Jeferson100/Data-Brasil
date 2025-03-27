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
	ruff check brazilian_data/*.py tests/*.py

pyright:
	pyright brazilian_data/*.py tests/*.py

ruff_format:
	ruff format brazilian_data/*.py tests/*.py

typemypy:
	mypy brazilian_data/ tests/

test:
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: uv_install lint ruff_lint format ruff_format pyright test
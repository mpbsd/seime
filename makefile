build:
	python3 -m pkgs.core

black:
	isort pkgs/core.py
	black -l 79 pkgs/core.py
	isort pkgs/date.py
	black -l 79 pkgs/date.py
	isort pkgs/regx.py
	black -l 79 pkgs/regx.py
	isort pkgs/serv.py
	black -l 79 pkgs/serv.py

clean:
	find . -type d -name __pycache__ | xargs rm -rf

ready:
	if [ ! -d brew ]; then \
		mkdir brew; \
	fi
	if [ -d venv ]; then \
		rm -rf venv; \
	fi
	python3 -m venv venv; \
	. venv/bin/activate; \
	pip install -U pip; \
	pip install -r requirements.txt; \
	deactivate

.PHONY: build black clean ready

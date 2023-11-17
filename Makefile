
install:
	pip install -r requirements.txt

run:
	python -B main.py

test:
	python -B -m pytest -v --cov-report term-missing --cov-fail-under=80 --cov=pkg ./tests	
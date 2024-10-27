all:
	echo "un truc"

test: lint unit-test
	coverage combine
	coverage report --fail-under=70 --skip-empty

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	pylint .

unit-test:
	coverage run --context=unit-test --data-file=.coverage.unit-test --branch --source=resources/lib/ --module pytest

service-test: %.py %.feature
	coverage run --context=service-test --data-file=.coverage.service-test --branch --source=resources/lib/ --module behave

clean:
	rm -r __pycache__ .pytest_cache .coverage*

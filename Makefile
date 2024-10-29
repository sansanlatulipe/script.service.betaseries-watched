ADDON_NAME := kodi.addon.name
ADDON_VERSION := 0.0.0
ADDON_PRERELEASE := $(shell echo $(ADDON_VERSION) | grep -Eq -- '\+.+$$' && echo true || echo false)
ADDON_ASSET := $(ADDON_NAME)_$(ADDON_VERSION).zip

all: test build

github-output:
	@echo "addon_name=$(ADDON_NAME)"
	@echo "addon_version=$(ADDON_VERSION)"
	@echo "addon_prerelease=$(ADDON_PRERELEASE)"
	@echo "addon_asset=$(ADDON_ASSET)"

build: clean
	@mkdir -p .build/$(ADDON_NAME) && cp -r * .build/$(ADDON_NAME)
	@(cd .build/$(ADDON_NAME) && rm -r behave.ini Dockerfile.dev Makefile pylintrc requirements*.txt resources/test/)
	@sed -i .build/$(ADDON_NAME)/addon.xml \
		-e "s/{{ addon_name }}/$(ADDON_NAME)/" \
		-e "s/{{ addon_version }}/$(ADDON_VERSION)/" \
		-e "/{{ addon_changelog }}/r changelog.txt" \
		-e "s/^.*{{ addon_changelog }}/$(ADDON_VERSION) (`date +'%Y-%m-%d'`)/"
	@(cd .build && zip -r $(ADDON_ASSET) $(ADDON_NAME))
	@rm -r .build/$(ADDON_NAME)

test-html: HTML_REPORT := --format=html --outfile=/var/www/html/behave-report.html
test-html: test

test: lint unit-test service-test
	@coverage combine
	@coverage report --fail-under=70 --skip-empty
	@[ -z "$(HTML_REPORT)" ] || coverage html --fail-under=70 --skip-empty --show-contexts --directory=/var/www/html/coverage

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --max-complexity=10 --max-line-length=120 --statistics
	pylint .

unit-test:
	@coverage run --context=unit-test --data-file=.coverage.unit-test --branch --source=resources/lib/ --module \
		pytest

service-test:
	coverage run --context=service-test --data-file=.coverage.service-test --branch --source=resources/lib/ --module \
		behave $(HTML_REPORT) --format=pretty

clean:
	@$(RM) -r .build/ .coverage* .pytest_cache/
	@find . -type d -name __pycache__ -exec rm -r {} +

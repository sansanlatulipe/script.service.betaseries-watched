ADDON_NAME := script.service.betaseries-watched
ADDON_VERSION := 0.0.0
ADDON_ASSET := $(ADDON_NAME)_$(ADDON_VERSION).zip

KODI_VERSION := matrix

all: lint test build

build: clean
	@echo "Create working directory"
	@mkdir -p .build/$(ADDON_NAME)
	@cp -r * .build/$(ADDON_NAME)
	@echo "Prepare addon asset contents"
	@(cd .build/$(ADDON_NAME) && rm -r behave.ini Dockerfile.dev Makefile resources/test/ pyproject.toml)
	@find .build/$(ADDON_NAME) -type d -exec chmod u=rwx,go=rx {} +
	@find .build/$(ADDON_NAME) -type f -exec chmod u=rw,go=r {} +
	@sed -ze "s/.*v$(ADDON_VERSION)[^\n]*\n\(\(- [^\n]\+\n\)\+\).*/\1/" changelog.txt > /tmp/changelog.txt
	@sed -i .build/$(ADDON_NAME)/addon.xml \
	    -e "s/{{ addon_name }}/$(ADDON_NAME)/" \
	    -e "s/{{ addon_version }}/$(ADDON_VERSION)/" \
	    -e "/{{ addon_changelog }}/r /tmp/changelog.txt" \
	    -e "/{{ addon_changelog }}/d"
	@rm /tmp/changelog.txt
	@echo "Build addon asset"
	@(cd .build/$(ADDON_NAME) && kodi-addon-checker --branch $(KODI_VERSION))
	@(cd .build && zip -r $(ADDON_ASSET) $(ADDON_NAME))
	@echo "Cleanup working directory"
	@rm -r .build/$(ADDON_NAME)

test-html: HTML_REPORT = --format=html --outfile=/var/www/html/behave-report.html
test-html: test

test: unit-test service-test
	@coverage combine
	@coverage report --fail-under=70 --skip-empty
	@coverage xml --skip-empty -o coverage.xml
	@[ -z "$(HTML_REPORT)" ] || coverage html --fail-under=70 --skip-empty --show-contexts --directory=/var/www/html/coverage

lint:
	@ruff check

unit-test:
	@coverage run --context=unit-test --data-file=.coverage.unit-test --branch --source=resources/lib/ --module \
	    pytest $(TEST_OPTIONS)

service-test:
	coverage run --context=service-test --data-file=.coverage.service-test --branch --source=resources/lib/ --module \
	    behave $(HTML_REPORT) --format=pretty $(TEST_OPTIONS)

clean:
	@rm -rf .build/ .?coverage* *.egg-info .pytest_cache/ .ruff_cache/
	@find . -type d -name __pycache__ -exec rm -r {} +

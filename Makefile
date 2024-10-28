ADDON_NAME := "kodi.addon.name"
ADDON_VERSION := "0.0.0"
ADDON_PRERELEASE := "$(shell echo $(ADDON_VERSION) | grep -Eq -- '\+.+$$' && echo true || echo false)"
ADDON_ASSET := "$(ADDON_NAME)_$(ADDON_VERSION).zip"

BUILD_DIR := ".build"
ADDON_BUILD := "$(BUILD_DIR)/$(ADDON_NAME)"

all: test build

github-output:
	@echo "addon_name=$(ADDON_NAME)"
	@echo "addon_version=$(ADDON_VERSION)"
	@echo "addon_prerelease=$(ADDON_PRERELEASE)"
	@echo "addon_asset=$(ADDON_ASSET)"

build: clean
	@mkdir -p $(ADDON_BUILD)
	@cp -r * $(ADDON_BUILD)
	@sed -i $(ADDON_BUILD)/addon.xml \
		-e "s/{{ addon_name }}/$(ADDON_NAME)/" \
		-e "s/{{ addon_version }}/$(ADDON_VERSION)/" \
		-e "/{{ addon_changelog }}/r changelog.txt" \
		-e "s/^.*{{ addon_changelog }}/$(ADDON_VERSION) (`date +'%Y-%m-%d'`)/"
	@(cd $(BUILD_DIR) && zip -r $(ADDON_ASSET) $(ADDON_NAME))
	@rm -r $(ADDON_BUILD)

test-html: test
	@coverage html --fail-under=70 --skip-empty --show-contexts --directory=/var/www/html/coverage

test: lint unit-test service-test
	@coverage combine
	@coverage report --fail-under=70 --skip-empty

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --max-complexity=10 --max-line-length=120 --statistics
	pylint .

unit-test:
	coverage run --context=unit-test --data-file=.coverage.unit-test --branch --source=resources/lib/ --module pytest

service-test:
	coverage run --context=service-test --data-file=.coverage.service-test --branch --source=resources/lib/ --module behave

clean:
	@$(RM) -r .pytest_cache .coverage* $(BUILD_DIR)
	@find . -type d -name __pycache__ -exec rm -r {} +

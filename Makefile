NAME := keybow

CIRCUITPY_DIR = /Volumes/CIRCUITPY
CIRCUITPY_DEFAULT_FILENAME = code.py

.PHONY: all
all: help

.PHONY: rainbow
rainbow: ## Copy rainbow-button code to CircuitPy device
	@echo use src/rainbow-buttons.py
	cp src/rainbow-buttons.py $(CIRCUITPY_DIR)/$(CIRCUITPY_DEFAULT_FILENAME)

.PHONY: hid-keys-advanced
hid-keys-advanced: ## Copy hid-keys-advanced code to CircuitPy device
	@echo use examples/hid-keys-advanced.py
	cp examples/hid-keys-advanced.py $(CIRCUITPY_DIR)/$(CIRCUITPY_DEFAULT_FILENAME)

.PHONY: huh
huh: ## Echos a 'huh'
	@echo 'huh'

.PHONY: help
help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


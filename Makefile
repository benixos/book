.PHONY: build serve check
build:
	python3 -I tools/build.py
check: build
	@echo "ok: built with no forbidden content and no broken local links"
serve: build
	cd docs && python3 -m http.server 8000

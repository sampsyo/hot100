hot100.html:
	python3 hot100.py > $@

.PHONY: open
open: hot100.html
	open hot100.html

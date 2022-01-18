decks:
	cd src && python3 main.py --file 'decks/Deck Builder.yaml'

install:
	python3 -m pip install .

.PHONY: decks
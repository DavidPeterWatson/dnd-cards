decks:
	cd src && python3 main.py --file 'decks/Deck Builder.yaml'

nyx:
	cdb build -f 'Decks/Nyx Daergel Deck.yaml'

damaia:
	cdb build -f 'Decks/Damaia Deck.yaml'

dm:
	cdb build -f "Decks/Dungeon Master's Deck.yaml"
install:
	python3 -m pip install .

.PHONY: decks, nyx

decks:
	cd src && python3 main.py --file 'decks/Deck Builder.yaml'

nyx:
	cdp print -f 'Decks/Nyx Daergel Deck.yaml'

damaia:
	cdp print -f 'Decks/Damaia Deck.yaml'

kathra:
	cdp print -f 'Decks/Kathra Rockseeker Deck.yaml'

dm:
	cdp print -f "Decks/Dungeon Master's Deck.yaml"

magicitems:
	cdp download -f 'Databases/Dnd5e Magic Items.yaml'

install:
	python3 -m pip install .

.PHONY: decks, nyx

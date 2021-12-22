dm:
	cd src && python3 deck.py --deck 'decks/Dungeon Master Deck.yaml'

damaia:
	cd src && python3 deck.py --deck 'decks/Damaia Deck.yaml'

.PHONY: dm, damaia
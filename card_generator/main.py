import generate_cards
import generate_decks
import generate_deck_objects

if __name__ == '__main__':
    generate_cards.run(overwrite=False)
    generate_decks.run()
    #generate_deck_objects.run()

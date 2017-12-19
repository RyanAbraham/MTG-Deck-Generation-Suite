# MTG Random Deck Generator
# Version 17.12.19
#
# To be used with Cockatrice

import os
import random
import sys
import json

# Path variables
JSON_NAME = 'AllCards.json'
# Set the deck path to save to
DECK_PATH = ""
DECK_NAME = 'ZZZCreated Deck.cod'
PROGRAMS = ['Random Deck Selector', 'Color Deck Generator', 'Land Generator']


def get_random_card(**kwargs):
    
    """Gets a random card from the parsed json.
    kwargs (dict) - Stores all attributes to search for in a card
    """
    
    card_str = ""
    card_str += '        <card number="1" price="0" name="'
    # After ten thousand search attempts, if none worked, it returns a failed search
    for i in range(10000):
        valid = True
        card = parsed_json[random.choice(list(parsed_json))]
        # For each attribute in kwargs, verify that the card matches the search query
        for key, value in kwargs.items():
            if (key == 'text'):
                # If it has no text, fails the search
                if (card.get(key) == None):
                    valid = False
                # If it has text, verify that it matches the query
                else:
                    # Loops through the list of search terms
                    # If a string was given, converts it a list with a single element in it
                    for query in value if not hasattr(value, 'lower') else [value]:
                        # If the search term can't be found
                        if (card.get('text').lower().find(query.lower()) == -1):
                            valid = False
            elif (key == 'cmc' or key == 'power' or key == 'toughness'):
                if (card.get(key) != value):
                    valid = False
            elif (key == 'types' or key == 'subtypes'):
                # Valid card if the search term is found at least once
                count = 0
                if (card.get(key) != None):
                    for element in card.get(key):
                        if (element.lower() == value.lower()):
                            count += 1
                if (count == 0):
                    valid = False
            elif (key == 'colors' or key =='colorIdentity'):
                # Valid card if search terms match exactly
                count = 0
                if (card.get(key) == None):
                    valid = False
                else:
                    for query in value if not hasattr(value, 'lower') else [value]:
                        for element in card.get(key):
                            if (element.lower() == value.lower()):
                                count += 1
                    if (count != len(card.get(key))):
                        valid = False
            else:
                print('Error: Unkown key \'' + key + '\'')
        if (valid):
            card_str += card.get('name')
            card_str += '"/>\n'
            return card_str
    sys.exit("SEARCH FAILED with parameters" + str(kwargs))
    return None

def random_deck():
    """Chooses one of your decks at random
    """
    deck = open(DECK_PATH + random.choice(os.listdir(DECK_PATH)))
    
    with open(DECK_PATH + "ZZZRandom Deck.cod", "w") as f:
        for line in deck:
            f.write(line)
    deck.close()

def color_gen(num):
    """Generates a random deck with [num] colors in it
    num (int) - Number of colors to generate for the deck
    """
    if (num < 1 or num > 5):
        sys.exit("INVALID NUMBER OF COLORS: " + str(num))
        return None
    cards = ""
    # Choose two random colors
    colors = random.sample(['w', 'u', 'b', 'r', 'g'], num)
    for color in colors:
        color_str = ''
        # Add basic lands
        if(color == 'w'):
            cards += '        <card number="10" price="0" name="Plains"/>\n'
            color_str += 'white'
        elif(color == 'u'):
            cards += '        <card number="10" price="0" name="Island"/>\n'
            color_str += 'blue'
        elif(color == 'b'):
            cards += '        <card number="10" price="0" name="Swamp"/>\n'
            color_str += 'black'
        elif(color == 'r'):
            cards += '        <card number="10" price="0" name="Mountain"/>\n'
            color_str += 'red'
        elif(color == 'g'):
            cards += '        <card number="10" price="0" name="Forest"/>\n'
            color_str += 'green'
        # Add non-lands
        for i in range(18):
            cards += get_random_card(colors = color_str)
    # Add dual/utility lands
    for i in range(4):
        cards += get_random_card(types = 'land', text = ['{'+colors[0]+'}', '{'+colors[1]+'}'])
    return cards

def land_gen(num):
    """Generates a random deck with [num] colors in it
    num (int) - Number of colors to generate for the deck
    """
    if (num < 1 or num > 5):
        sys.exit("INVALID NUMBER OF COLORS: " + str(num))
        return None
    cards = ""
    # Choose two random colors
    colors = random.sample(['w', 'u', 'b', 'r', 'g'], num)
    for color in colors:
        color_str = ''
        if(color == 'w'):
            color_str += 'white'
        elif(color == 'u'):
            color_str += 'blue'
        elif(color == 'b'):
            color_str += 'black'
        elif(color == 'r'):
            color_str += 'red'
        elif(color == 'g'):
            color_str += 'green'
        # Add non-lands
        for i in range(18):
            cards += get_random_card(colors = color_str)
    # Add dual/utility lands
    for i in range(14):
        cards += get_random_card(types = 'land', text = ['{'+colors[0]+'}', '{'+colors[1]+'}'])
    for i in range(10):
        cards += get_random_card(types = 'land')
    return cards


def choose_program():
    """ Takes in user input to choose a program to run
    """
    input_str = 'Welcome to the Deck Generation Suite! Choose a program to run:'
    for i, program in enumerate(PROGRAMS):
        input_str += '\n' + str(i+1) + ': ' + program
    while (True):
        user_input = input(input_str + '\n')
        if (user_input.isdigit()):
            return int(user_input)


if __name__ == "__main__":
    # Parsing the json database
    json_file = open(JSON_NAME)
    json_cards = json_file.read()
    parsed_json = json.loads(json_cards)
    json_file.close()

    program = choose_program()

    # Starting off the Cockatrice deck file
    deck = ['<?xml version="1.0" encoding="UTF-8"?>\n', '<cockatrice_deck version="1">\n', '    <deckname></deckname>\n', '    <comments></comments>\n', '    <zone name="main">\n']

    # Run the chosen deck generation program
    if (program == 1):
        random_deck()
    if (program == 2):
        deck.append(color_gen(2))
    if (program == 3):
        deck.append(land_gen(2))

    # Ending the Cockatrice deck file
    deck.append('    </zone>\n')
    deck.append('</cockatrice_deck>\n')

    # Now write to the deck file
    with open(DECK_PATH + DECK_NAME, "w") as f:
        for line in deck:
            f.write(line)

    print("Deck generated in %s" % DECK_PATH)

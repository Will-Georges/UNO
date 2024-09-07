"""Imports"""
import random

"""Variables"""
deck = []
discard_pile = []
colours = ["Red", "Green", "Yellow", "Blue"]
values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]

deck_one = []
deck_two = []

deck_one_turn = True
name1 = input("What is Player 1's Name? ")
name2 = input("What is Player 2's Name? ")


def setup():
    """Set the initial deck"""
    global deck
    for colour in colours:
        for value in values:
            card_value = colour + " " + value
            deck.append(card_value)
            if value != "0":
                deck.append(card_value)
    for i in range(4):
        deck.append("Wild Color")
        deck.append("Wild +4")
    random.shuffle(deck)


def play():
    """Set the initial decks"""
    draw_card(deck_one, 7)
    draw_card(deck_two, 7)
    print("To draw a card, type 'draw'")
    """Set the first card"""
    i = 0
    discard_pile.append(deck[i])
    """Make sure the first card isn't a wild card"""
    while "Wild" in discard_pile[len(discard_pile) - 1]:
        i += 1
        discard_pile.append(deck[i])
    """Start the game"""
    show_turn_dialogue(deck_one, name1)


def show_turn_dialogue(hand, name):
    """Print information for the user"""
    global deck_one_turn
    print("---------------------------------------------------------------------------------------------------------")
    print("Current Card: " + str(discard_pile[len(discard_pile) - 1]))
    print(name + "'s deck: " + ", ".join(hand))
    card = input("Which card would you like to place? ")
    """Check if the play wants to draw a card"""
    if card == "draw":
        """First check if they already have a card to play"""
        if has_card_to_play(hand):
            card = input("You have a card to play. Do you want to play it? (yes/no)")
            if card.lower() == "yes":
                card_to_play = input("Which card would you like to play? ")
                """Play the card they select"""
                if card_to_play in hand and can_place_card(card_to_play):
                    hand.remove(card_to_play)
                    discard_pile.append(card_to_play)
                    print(name + " played " + card_to_play + ". Turn moves to the other player.")
                    deck_one_turn = not deck_one_turn
                    if deck_one_turn:
                        show_turn_dialogue(deck_one, name1)
                    else:
                        show_turn_dialogue(deck_two, name2)
                else:
                    print("Invalid card or cannot be placed. Try again.")
                    show_turn_dialogue(hand, name)
            else:
                can_play_drawn_card(hand, name)
        else:
            can_play_drawn_card(hand, name)

    """Check if the card they enter is in their hand"""
    if card in hand:
        """Check if they can legally place the card"""
        if can_place_card(card):
            """Functionality for +2 cards"""
            if "+2" in card:
                if deck_one_turn:
                    draw_card(deck_two, 2)
                else:
                    draw_card(deck_one, 2)

            """Reverse functionality is the same as skip for 2 player"""
            if "Reverse" in card or "Skip" in card:
                hand.remove(card)
                discard_pile.append(card)
                if deck_one_turn:
                    show_turn_dialogue(deck_one, name1)
                else:
                    show_turn_dialogue(deck_two, name2)

            """Check if the card is a wild"""
            if "Wild" in card:
                hand.remove(card)
                """Get the user to input a color"""
                color = input("What color do you want to pick? ")
                while color != "Red" and color != "Blue" and color != "Green" and color != "Yellow":
                    color = input("Invalid. Pick: Red, Green, Yellow or Blue ")
                discard_pile.append(color + " Color")
                deck_one_turn = not deck_one_turn
                """Check if the wild is also a +4"""
                if deck_one_turn:
                    if "+4" in card:
                        draw_card(deck_one, 4)
                    show_turn_dialogue(deck_one, name1)
                else:
                    if "+4" in card:
                        draw_card(deck_two, 4)
                    show_turn_dialogue(deck_two, name2)

            hand.remove(card)
            discard_pile.append(card)
            """Check if a player has won"""
            if len(hand) <= 0:
                end_game(name)
            deck_one_turn = not deck_one_turn
            if deck_one_turn:
                show_turn_dialogue(deck_one, name1)
            else:
                show_turn_dialogue(deck_two, name2)
        else:
            print("Invalid card. Try again.")
            show_turn_dialogue(hand, name)
    else:
        print("You don't have that card. Try again.")
        show_turn_dialogue(hand, name)


def can_play_drawn_card(hand, name):
    """Checks if the card that was drawn can be placed"""
    global deck_one_turn
    drawn_cards = draw_card(hand, 1)
    drawn_card = drawn_cards[0]
    print(name + " drew a card: " + str(drawn_card))
    """Place the card if it can legally be placed"""
    if can_place_card(drawn_card):
        hand.remove(drawn_card)
        discard_pile.append(drawn_card)
        print("The drawn card was placed. Turn moves to the other player.")
    else:
        print("The drawn card cannot be placed. Turn moves to the other player.")
    deck_one_turn = not deck_one_turn
    if deck_one_turn:
        show_turn_dialogue(deck_one, name1)
    else:
        show_turn_dialogue(deck_two, name2)


def has_card_to_play(hand):
    """Checks that when the player asks to draw, if they already hae a card that they can play"""
    for card in hand:
        if can_place_card(card):
            return True
    return False


def can_place_card(card):
    """Checks if they can place a card"""
    top_card = discard_pile[len(discard_pile) - 1]
    card_color, card_value = card.split()
    top_card_color, top_card_value = top_card.split()
    return card_color == top_card_color or card_value == top_card_value or card_color == "Wild"


def end_game(name):
    """Functionality for handling when the game ends"""
    global deck, discard_pile, deck_one, deck_two, deck_one_turn
    print("---------------------------------------------------------------------------------------------------------")
    print(name + " has won the game! To play again, type play again. To end the game, type end")
    response = input("play again or end: ")
    if response == "play again":
        deck = []
        discard_pile = []
        deck_one = []
        deck_two = []
        deck_one_turn = True
        setup()
        play()
    else:
        print("Game Ended")
        exit()


def draw_card(hand, num):
    """Draws a card"""
    global deck
    cards_drawn = []
    for i in range(num):
        card = deck[i]
        hand.append(card)
        deck.remove(card)
        cards_drawn.append(card)  # Add drawn card to the list
    return cards_drawn  # Return list of cards drawn


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup()
    play()

# Simulate a card battle between two players.
# Shuffle the deck and split it in half.
# Each player will have half of the deck respectively as their "battle deck".
# Players will then draw the top card of their battle deck, play it, and then compare results.
# Player that played the higher value card will then keep both of the played cards as score under the "captured deck".

from typing import List


def main() -> None:
    # Figure out how many players will be playing so we can split the deck + deal accordingly.
    num_players = input("How many players will be playing?")
    while not num_players.isnumeric or (num_players.isnumeric and num_players < 2):
        print("Please input a numeric value greater than or equal to 2.")
        
        num_players = input("How many players will be playing?")


    # Simulate the shuffling and dealing here.

    # Deck consists of the numbers 1-12 with 5 copies of each, deck size is 5*num_players.
    base_deck = [1,2,3,4,5,6,7,8,9,10,11,12]
    for i in range(num_players):
        

    # Probably create a function for shuffling s.t. it will be called multiple times
    # throughout the game; it will shuffle regardless of deck size.
    # e.g. shuffle the player's "captured deck" when their "battle deck" is empty,
    # and that "captured deck" is now their new "battle deck".
    deck_shuffle(game_deck)


    for i in range(num_players):
        print()
    # Initialize each player's drawn card.

    p1_card = p1_battledeck.pop()
    p2_card = p2_battledeck.pop()
    print("Player 1 plays the %s card, ", p1_card)
    return

def deck_shuffle(deck: List[int]) -> list:
    # Do the shuffling here. Move the contents of the list/array randomly within itself.
    return deck
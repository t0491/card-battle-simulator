# Simulate a card battle between two players.
# Shuffle the deck and split it in half.
# Each player will have half of the deck respectively as their "battle deck".
# Players will then draw the top card of their battle deck, play it, and then compare results.
# Player that played the higher value card will then keep both of the played cards as score under the "captured deck".

from typing import Dict, List
import numpy
from numpy.lib.shape_base import split


class Player:
    my_id = None # Used for identifying which player this is in a BR scenario once others are elim'd/deleted.
    my_deck = [] # Contains the person's battle deck.
    my_hand = [] # Holds the players drawn cards before playing.
    captured_deck = [] # Points/captured cards. Will be used as battle deck once that is empty.
    bot_ai = None # Configured for random or high value priority.
    played_card = None
        
    # Init for the Player
    def __init__(self, my_id, my_deck, bot_ai) -> None:
        self.my_id = my_id
        self.my_deck = my_deck
        self.bot_ai = bot_ai

    # Returns the player's battle deck.
    def get_bd(self) -> list:
        return self.my_deck

    # Return the player's captured deck.
    def get_cd(self) -> list:
        return self.captured_deck

    # Takes the top card out of their battle deck and adds it into their hand.
    def draw_card(self) -> None:
        self.my_hand.append(self.my_deck.pop())
    
    # Sets the inputted card as the player's played_card and returns a "copy" of it.
    def play_card(self, card: int) -> int:
        self.my_hand.remove(card) # Remove that card from the player's hand, it has been played.
        self.played_card = card
        return self.played_card

    def show_hand(self) -> list:
        return self.my_hand

def main() -> None:
    
    # Prompts user for # of players to setup the game.
    num_players = acquire_players()

    # Generates the deck based on # of players + shuffles it.
    game_deck = create_deck(num_players)
    
    # Split the deck into equal parts for the players.
    split_deck = numpy.array_split(game_deck, num_players)

    # Initialize a dictionary containing all players, we Key them with their IDs.
    player_list = {}

    # Give them their decks as well.
    for i in range(num_players):
        player_list[i+1] = Player(i+1, split_deck[i], None)

    #print(player_list[1].get_bd())

    #print("Player 1 plays the %s card, ", p1_card)
    
    # Begin running the battle simulation.
    start_simulation(player_list)
    return

def acquire_players() -> int:
    # Figure out how many players will be playing so we can split the deck + deal accordingly.
    num_players = input("How many players will be playing?")
    while not num_players.isnumeric() or (num_players.isnumeric() and int(num_players) < 2):
        print("Please input a numeric value greater than or equal to 2.")
            
        num_players = input("How many players will be playing?")

    # Confirm num_players is now an integer rather than an string containing a number.
    return int(num_players)

def create_deck(num_players: int) -> list:
    # Deck consists of the numbers 1-12 with num_players copies of each, deck size is 12*num_players.
    base_deck = [1,2,3,4,5,6,7,8,9,10,11,12]
    game_deck = []
    for _ in range(num_players):
        for i in base_deck:
            game_deck.append(i)

    # Probably create a function for shuffling s.t. it will be called multiple times
    # throughout the game; it will shuffle regardless of deck size.
    # e.g. shuffle the player's "captured deck" when their "battle deck" is empty,
    # and that "captured deck" is now their new "battle deck".
    deck_shuffle(game_deck)
    #print(game_deck)
    return game_deck

def deck_shuffle(deck: List[int]) -> list:
    # Do the shuffling here. Move the contents of the list/array randomly within itself.
    return numpy.random.shuffle(deck)

def start_simulation(player_list: Dict) -> None:
    # A list that keeps track of the remain players' IDs
    # Once a player is eliminated, find their index and delete them.
    remaining_players = []
    for i in range(player_list):
        remaining_players[i] = [i+1]

    # Keep playing until there is 1 remaining player.
    while len(remaining_players) > 1:

        # Draw and play the card here.
        for players in player_list:
            # Simulates playing with only top decking.
            players.draw_card() # This card enters the player's hand.
            players.play_card(players.my_hand()[0]) # Plays the first drawn card from their hand.
        
        # Compare the played card results here.
        for players in player_list:
            

    return

main()
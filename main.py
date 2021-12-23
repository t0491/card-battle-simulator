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
    
    # Sets the inputted card as the player's played_card.
    def play_card(self, card: int) -> int:
        self.my_hand.remove(card) # Remove that card from the player's hand, it has been played.
        self.played_card = card

    def show_played_card(self) -> int:
        return self.played_card

    def show_hand(self) -> list:
        return self.my_hand

    def show_id(self) -> int:
        return self.my_id

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
        player_list[i+1] = Player(i+1, split_deck[i].tolist(), None)

    #print("Player 1 plays the %s card, ", p1_card)
    
    # Begin running the battle simulation.
    start_simulation(player_list)
    return

def acquire_players() -> int:
    # Figure out how many players will be playing so we can split the deck + deal accordingly.
    num_players = input("How many players will be playing? ")
    while not num_players.isnumeric() or (num_players.isnumeric() and int(num_players) < 2):
        print("Please input a numeric value greater than or equal to 2.")
            
        num_players = input("How many players will be playing? ")

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

    # Keep playing until there is 1 remaining player.
    round_counter = 1
    while len(player_list) > 1:

        # Keeps track of the current winner/highest, if size > 1 then there's a tie.
        round_winner = []
        print("### Round " + str(round_counter)+ " ###")

        # Draw and play the card here.
        for player in player_list.values():
            # Simulates playing with only top decking.
            player.draw_card() # This card enters the player's hand.
            player.play_card(player.show_hand()[0]) # Plays the first drawn card from their hand.
        
        # Compare the played card results here.
        highest_card = 0
        pooled_cards = []
        for player in player_list.values():
            print("Player #" + str(player.show_id()) + " plays, " + str(player.show_played_card()) + "!")
            # Update the new highest card.
            if player.show_played_card() > highest_card:
                highest_card = player.show_played_card()
                round_winner.clear() # Clear the array of all previous winners/ties if there's a new higher value.
                round_winner.append(player.show_id()) # Add the updated winner to the list.

            elif player.show_played_card() == highest_card:
                round_winner.append(player.show_id()) # Add another winner into the list for a tie.

            # If you're less than the highest card, give up your card.
            else:
                pooled_cards.append(player.show_played_card())
        
        if len(round_winner) > 1:
            # Execute the tiebreaker here, perhaps recurses until the tie finally resolves.
            exe_tiebreaker(player_list, round_winner)

        # Check player deck/resources now. If they are 0, then the player is eliminated.
        for players in player_list.values():
            if players.get_bd() == 0 and players.get_cd() == 0:
                player_list.pop(players.show_id())
        
        # Give the winner all the pooled cards and their played card (they "lost" their played card earlier when they played it).
        round_counter += 1
        break

    return

# Returns the ID of the tie winner, may recurse.
# If it does recurse, the new inputted round_winner will dwindle down and remove any losers of the tiebreaker.
def exe_tiebreaker(player_list: Dict, round_winner: List[int]) -> int:
    return

main()
# Simulate a card battle between two players.
# Shuffle the deck and split it in half.
# Each player will have half of the deck respectively as their "battle deck".
# Players will then draw the top card of their battle deck, play it, and then compare results.
# Player that played the higher value card will then keep both of the played cards as score under the "captured deck".

from typing import Dict, List
import numpy
import random

class Player: 
    # Init for the Player
    def __init__(self, my_id, my_deck, bot_ai) -> None:
        self.my_id = my_id # Used for identifying which player this is in a BR scenario once others are elim'd/deleted.
        self.my_deck = my_deck # Contains the person's battle deck.
        self.bot_ai = bot_ai
        self.my_hand = [] # Holds the players drawn cards before playing.
        self.captured_deck = [] # Points/captured cards. Will be used as battle deck once that is empty.
        self.bot_ai = bot_ai # Configured for random or high value priority.
        self.played_card = None

    # Returns the player's battle deck.
    def get_bd(self) -> list:
        return self.my_deck

    # Return the player's captured deck.
    def get_cd(self) -> list:
        return self.captured_deck

    def get_ai(self) -> str:
        if self.bot_ai == None:
            return "Top-deck"
        elif self.bot_ai == 1:
            return "Random"
        elif self.bot_ai == 2:
            return "Highest"

    # Takes the top card out of their battle deck and adds it into their hand.
    def draw_card(self) -> None:
        self.my_hand.append(self.my_deck.pop())
    
    # Sets the inputted card as the player's played_card.
    def play_card(self) -> int:
        if self.bot_ai == None: # Top-deck AI
            self.played_card = self.my_hand.pop(0) # Remove the first card in hand.
        elif self.bot_ai == 1: # Random AI
            self.played_card = self.my_hand.pop(random.randint(0,len(self.my_hand)-1)) # Choose a random card (index) in their hand.
        elif self.bot_ai == 2: # Highest Val AI
            """ THIS WORKS PROPERLY, I WAS CONFUSED AT FIRST SEEING THAT THE AI PLAYED A HIGHER VALUE CARD
                THAN THE PREVIOUS ROUND, BUT IT WAS BECAUSE IT JUST DREW INTO THE HIGHER VALUE CARD.
                e.g. ROUND 1 PLAYS: 11
                     ROUND 2 PLAYS: 12
                HAND WAS [11, 2, 3, 4, 5] AT ROUND 1 BUT ROUND 2 IT DREW INTO 12 SO IT BECAME [2, 3, 4, 5, 12]"""
            highest_card = max(self.my_hand) # Determine highest value.
            #print(highest_card)
            self.played_card = highest_card
            self.my_hand.remove(max(self.my_hand)) # Remove that specific card from hand once played.
    
    # Allocates all of the round winnings into the player's win pile/captured deck.
    def capture_card(self, card: int) -> None:
        self.captured_deck.append(card)

    def show_played_card(self) -> int:
        return self.played_card

    def show_hand(self) -> list:
        return self.my_hand

    def show_id(self) -> int:
        return self.my_id

    # Copy over all of the captured cards to battle and then clear the captured.
    def transfer_cd_to_bd(self) -> int:
        self.my_deck = self.captured_deck.copy()
        self.captured_deck.clear()

def main() -> None:
    
    # Prompts user for # of players to setup the game.
    num_players = acquire_players()

    # Determines if we are doing top-deck or strategic.
    ai_style = []
    game_mode = acquire_game_mode()

    # Top-deck, then there is no AI choice pattern.
    if game_mode == 1:
        for i in range(num_players):
            ai_style.append(None)
    # Strategic, we allocate them as Random(1) or Highest Value(2) then.
    elif game_mode == 2:
        for i in range(num_players):
            ai_style.append(random.randint(1,2))

    # Generates the deck based on # of players + shuffles it.
    game_deck = create_deck(num_players)
    
    # Split the deck into equal parts for the players.
    split_deck = numpy.array_split(game_deck, num_players)

    # Initialize a dictionary containing all players, we Key them with their IDs.
    player_list = {}

    # Give them their decks as well.
    for i in range(num_players):
        player_list[i+1] = Player(i+1, split_deck[i].tolist(), ai_style[i])

    for player in player_list.values():
        print("Player #" + str(player.show_id()) + "'s AI is " + player.get_ai())

    # Begin running the battle simulation.
    start_simulation(player_list, game_mode)
    return

def acquire_game_mode() -> int:
    game_mode = input("What type of simulation would you like? \n1: Top-deck (AI plays first card drawn) \n" 
                + "2: Strategic (AI plays randomly or highest value card from a hand of 5) \nEnter here: ")
    while not game_mode.isnumeric() or (game_mode.isnumeric() and int(game_mode) < 1) or (game_mode.isnumeric() and int(game_mode) > 2):
        print("Please input the number 1 or 2 based on your selection.")

        game_mode = input("What type of simulation would you like? \n1: Top-deck (AI plays first card drawn) \n" 
                + "2: Strategic (AI plays randomly or highest value card from a hand of 5) \nEnter here: ")
    
    return int(game_mode)
    
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

def start_simulation(player_list: Dict, game_mode: int) -> None:

    round_counter = 1
    # Keeps track of the current winner/highest, if size > 1 then there's a tie.
    round_winner = []
    # Keeps track of current winnings pool.
    pooled_cards = []

    # Keep playing until there is 1 remaining player.
    while True:
        # Removes any players with no cards remaining.
        eliminate_empty_players(player_list)

        # Breaks the while loop and ends the game once there is one player remaining.
        if len(player_list) < 2:
            break

        print("### Round " + str(round_counter)+ " ###")

        # Keeps track of current highest value card.
        highest_card = 0

        # Draw and play the card here.
        for player in player_list.values():
            
            # Only draw if they have cards left in their battle deck.
            # If they don't then they should still have cards left in their hand to play.
            # They would have been eliminated if their hand, bd, and cd were all empty.
            if len(player.get_bd()) > 0:
                # Set up by having each player draw 5 cards in their hand at first if strategic.
                if game_mode == 2 and round_counter == 1:
                    for _ in range(5):
                        player.draw_card()
                # Otherwise it doesn't matter and they'll play top-deck.
                else:
                    player.draw_card()
            player.play_card() # Play the card according to their AI

            # print the hand below if you want to check and see if the AI is playing correctly by their "bot_ai"
            # print("Player #" + str(player.show_id() + "'s hand: " + player.show_hand())
            print("Player #" + str(player.show_id()) + " plays, " + str(player.show_played_card()) + "!")

            # Compare the played card results here.
            # Update the new highest card.
            if player.show_played_card() > highest_card:
                highest_card = player.show_played_card()
                round_winner.clear() # Clear the array of all previous winners/ties if there's a new higher value.
                round_winner.append(player.show_id()) # Add the updated winner to the list.

            elif player.show_played_card() == highest_card:
                round_winner.append(player.show_id()) # Add another winner into the list for a tie.

            # Everyone pools their cards into the middle per play.
            pooled_cards.append(player.show_played_card())

        if len(round_winner) > 1:
            # Execute the tiebreaker here, perhaps recurses until the tie finally resolves.
            round_winner = exe_tiebreaker(player_list, round_winner, pooled_cards)

        # Checks to see current winnings so far.
        print("Pooled Cards: " + str(pooled_cards))
        print("Round Winner: " + str(round_winner[0]))

        # Give the winner all the pooled cards.
        for card in pooled_cards:
            # Indexed/key'd the player using the round_winner ID.
            player_list[round_winner[0]].get_cd().append(card)

        print("Remaining Players: " + str(len(player_list)))

        round_counter += 1
        round_winner.clear() # Empty it between every round.
        pooled_cards.clear()
    
    # Should only print once for the last remaining player.
    for player in player_list.values():
        print("### GAME OVER ###")
        print("Player #" + str(player.show_id()) + " is the winner of Card Battle Royale!")

        # Should total up to 12 * num_players.
        print("They have collected all " + str(len(player.get_bd()) + len(player.get_cd()) + len(player.show_hand())) + " cards!")
    return

# Returns the ID of the tie winner, may recurse.
# If it does recurse, the new inputted round_winner will dwindle down and remove any losers of the tiebreaker.
def exe_tiebreaker(player_list: Dict, old_round_winner: List[int], pooled_cards: List[int]) -> list:
    
    # Removes any players with no cards remaining.
    eliminate_empty_players(player_list)

    highest_card = 0
    round_winner = []
    # End the tiebreaker phase if there are no other players to play.
    # Return the last remaining player as the round_winner
    if len(player_list) < 2:
        for player in player_list.values():
            round_winner.append()
        return round_winner

    print("### TIE BREAKER ###")
    for player in player_list.values():
        #print(len(player_list))
        if player.show_id() in old_round_winner:

            # Draw and play the card here.
            # Once again, only draw if there are cards left in bd.
            if len(player.get_bd()) > 0:
                player.draw_card()
            player.play_card()
        
            # Compare the played card results here.
            print("Player #" + str(player.show_id()) + " plays, " + str(player.show_played_card()) + "!")
            # Update the new highest card.
            if player.show_played_card() > highest_card:
                highest_card = player.show_played_card()
                round_winner.clear() # Clear the array of all previous winners/ties if there's a new higher value.
                round_winner.append(player.show_id()) # Add the updated winner to the list.

            elif player.show_played_card() == highest_card:
                round_winner.append(player.show_id()) # Add another winner into the list for a tie.

            pooled_cards.append(player.show_played_card())

    print("Remaining Players: " + str(len(player_list)))
    
    if len(round_winner) > 1:
        round_winner = exe_tiebreaker(player_list, round_winner, pooled_cards)

    # In order for the recursion to stop, the returned round winner must be a size of 1.
    return round_winner

def eliminate_empty_players(player_list: Dict) -> None:
    # Check player deck/resources now. If they are 0, then the player is eliminated.
    to_be_elimd = []
    for player in player_list.values():
        # If they have captured cards, turn it into their battle cards.
        if len(player.get_bd()) == 0 and len(player.get_cd()) > 0:
            player.transfer_cd_to_bd()
            deck_shuffle(player.get_bd()) # Shuffle it afterwards.
        # If they still have cards in their battle deck or in their hand, they aren't eliminated.
        elif len(player.get_bd()) > 0 or len(player.show_hand()) > 0:
            continue
        # If both decks empty, eliminate.
        elif len(player.get_bd()) == 0 and len(player.get_cd()) == 0:
            to_be_elimd.append(player.show_id())

    for i in to_be_elimd:
        player_list.pop(i)
    
    return
main()
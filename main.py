from typing import Dict, List
import numpy
import random

class Player: 
    # Init for the Player
    def __init__(self, my_id, battle_deck, bot_ai) -> None:
        self.my_id = my_id # Used for identifying which player this is in a BR scenario once others are elim'd/deleted.
        self.battle_deck = battle_deck # Contains the person's battle deck.
        self.captured_deck = [] # Points/captured cards. Will be used as battle deck once that is empty.
        self.my_hand = [] # Holds the players drawn cards before playing.
        self.played_card = None
        self.bot_ai = bot_ai # Configured for random or high value priority.
        # Set up by having each player draw 4 cards in their hand at first if it's not top-deck.
        if self.bot_ai != 1:
            for _ in range(4):
                self.draw_card()
        # Otherwise they'll draw their top-deck card in start_sim()

    def get_id(self) -> int:
        return self.my_id

    # Returns the player's battle deck.
    def get_bd(self) -> list:
        return self.battle_deck

    # Return the player's captured deck.
    def get_cd(self) -> list:
        return self.captured_deck

    def get_hand(self) -> list:
        return self.my_hand
        
    def get_played_card(self) -> int:
        return self.played_card

    def get_ai(self) -> str:
        if self.bot_ai == 1:
            return "Top-deck"
        elif self.bot_ai == 2:
            return "Random"
        elif self.bot_ai == 3:
            return "Highest"
        elif self.bot_ai == None:
            return "Real Player"

    # Copy over all of the captured cards to battle and then clear the captured.
    def transfer_cd_to_bd(self) -> None:
        self.battle_deck = self.captured_deck.copy()
        self.captured_deck.clear()

    # Takes the top card out of their battle deck and adds it into their hand.
    def draw_card(self) -> None:
        # If their battle deck is empty but they have captured cards, turn it into their battle cards.
        if len(self.battle_deck) == 0 and len(self.captured_deck) > 0:
            self.transfer_cd_to_bd()
            deck_shuffle(self.battle_deck) # Shuffle it afterwards.

        # You can only draw if you have cards left in your battle deck.
        if len(self.battle_deck) > 0:
            self.my_hand.append(self.battle_deck.pop())
    
    # Sets the inputted card as the player's played_card depending on the AI.
    def play_card(self) -> None:
        if self.bot_ai == 1: # Top-deck AI
            self.played_card = self.my_hand.pop(0) # Remove the first card in hand.
        elif self.bot_ai == 2: # Random AI
            self.played_card = self.my_hand.pop(random.randint(0,len(self.my_hand)-1)) # Choose a random card (index) in their hand.
        elif self.bot_ai == 3: # Highest Val AI
            """ THIS WORKS PROPERLY, I WAS CONFUSED AT FIRST SEEING THAT THE AI PLAYED A HIGHER VALUE CARD
                THAN THE PREVIOUS ROUND, BUT IT WAS BECAUSE IT JUST DREW INTO THE HIGHER VALUE CARD.
                e.g. ROUND 1 PLAYS: 11
                     ROUND 2 PLAYS: 12
                HAND WAS [11, 2, 3, 4, 5] AT ROUND 1 BUT ROUND 2 IT DREW INTO 12 SO IT BECAME [2, 3, 4, 5, 12]"""
            highest_card = max(self.my_hand) # Determine highest value.
            #print(highest_card)
            self.played_card = highest_card
            self.my_hand.remove(max(self.my_hand)) # Remove that specific card from hand once played.

        elif self.bot_ai == None: # Real Player
            card_choice = self.choose_card() # Obtain what card the player wants to use.
            self.played_card = card_choice
            self.my_hand.remove(card_choice)

    # Only called when a Real Player is on their "play card" phase.
    def choose_card(self) -> int:
        print(self.my_hand) # Show the player their hand to choose from.
        card_choice = input("What card would you like to play from your hand? ")

        while not card_choice.isnumeric() or (card_choice.isnumeric() and not(int(card_choice) in self.my_hand)):
            print("Please choose a real card from your hand and input its value, not index.")
            
            card_choice = input("What card would you like to play from your hand? ")

        return int(card_choice)

    # Allocates all of the round winnings into the player's win pile/captured deck.
    def capture_card(self, card: int) -> None:
        self.captured_deck.append(card)

def acquire_game_mode() -> int:
    game_mode = input("What type of game mode would you like? \n1: Play vs. Bots \n"
                + "2: Simulate Bot vs. Bot \nEnter here: ")
    while not game_mode.isnumeric() or (game_mode.isnumeric() and int(game_mode) < 1) or (game_mode.isnumeric() and int(game_mode) > 2):
        print("Please input the number 1 or 2 based on your selection.")  

        game_mode = input("What type of game mode would you like? \n1: Play vs. Bots \n"
                + "2: Simulate Bot vs. Bot \nEnter here: ")      

    # Let the user know who they are.
    if int(game_mode) == 1:
        print("You will be referred to as Player #1 for the game.")

    return int(game_mode)
    
def acquire_bots(game_mode) -> int:
    # Figure out how many bots will be playing so we can split the deck + deal accordingly.
    num_bots = input("How many bots will be playing? ")

    if game_mode == 1: # Only requires 1 bot (opponent) if the user is playing themselves.
        while not num_bots.isnumeric() or (num_bots.isnumeric() and int(num_bots) < 1):
            print("Please input a numeric value greater than or equal to 1.")
            num_bots = input("How many bots will be playing? ")

    elif game_mode == 2: # Requires at least 2 bots to start a simulation since user isn't playing.
        while not num_bots.isnumeric() or (num_bots.isnumeric() and int(num_bots) < 2):
            print("Please input a numeric value greater than or equal to 2.")
            num_bots = input("How many bots will be playing? ")

    # Confirm num_players is now an integer rather than an string containing a number.
    return int(num_bots)

def acquire_ai_type() -> int:
    ai_type = input("What type of AI would you like? \n1: Top-deck (AI plays first card drawn) \n" 
                + "2: Strategic (AI plays randomly or highest value card from a hand of 5) \nEnter here: ")
    while not ai_type.isnumeric() or (ai_type.isnumeric() and int(ai_type) < 1) or (ai_type.isnumeric() and int(ai_type) > 2):
        print("Please input the number 1 or 2 based on your selection.")

        ai_type = input("What type of simulation would you like? \n1: Top-deck (AI plays first card drawn) \n" 
                + "2: Strategic (AI plays randomly or highest value card from a hand of 5) \nEnter here: ")
    return int(ai_type)

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

def eliminate_empty_players(player_list: Dict) -> None:
    # Check player deck/resources now. If they are 0, then the player is eliminated.
    to_be_elimd = []
    for player in player_list.values():
        # If both decks and hand are empty, eliminate them.
        if len(player.get_bd()) == 0 and len(player.get_cd()) == 0 and len(player.get_hand()) == 0:
            to_be_elimd.append(player.get_id())

    for i in to_be_elimd:
        player_list.pop(i)
    
    return

def play_round(player: Player, highest_card: int, round_winner: List[int], pooled_cards: List[int]) -> int:
    # Draw and play the card here.
    player.draw_card()

    # Real Players get to choose their card in here, refer to .play_card() definition.
    player.play_card() # Play the card according to their AI

    # print the hand below if you want to check and see if the AI is playing correctly by their "bot_ai"
    # print("Player #" + str(player.get_id() + "'s hand: " + player.get_hand())
    print("Player #" + str(player.get_id()) + " plays, " + str(player.get_played_card()) + "!")

    # Compare the played card results here.
    # Update the new highest card.
    if player.get_played_card() > highest_card:
        highest_card = player.get_played_card()
        round_winner.clear() # Clear the array of all previous winners/ties if there's a new higher value.
        round_winner.append(player.get_id()) # Add the updated winner to the list.

    elif player.get_played_card() == highest_card:
        round_winner.append(player.get_id()) # Add another winner into the list for a tie.

    # Everyone pools their cards into the middle per play.
    pooled_cards.append(player.get_played_card())

    return highest_card

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
            round_winner.append(player)
        return round_winner

    print("### TIE BREAKER ###")

    for player in player_list.values():
        # Only the winners of the previous round (the ones that tied) will be playing now.
        if player.get_id() in old_round_winner:
            highest_card = play_round(player, highest_card, round_winner, pooled_cards)

    #print("Remaining Players: " + str(len(player_list)))

    if len(round_winner) > 1:
        round_winner = exe_tiebreaker(player_list, round_winner, pooled_cards)

    # In order for the recursion to stop, the returned round winner must be a size of 1.
    return round_winner

def start_simulation(player_list: Dict) -> None:

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

        # Each player will go through the play phase of the game.
        for player in player_list.values():
            highest_card = play_round(player, highest_card, round_winner, pooled_cards)

        if len(round_winner) > 1:
            # Execute the tiebreaker here, perhaps recurses until the tie finally resolves.
            round_winner = exe_tiebreaker(player_list, round_winner, pooled_cards)

        # Checks to see current winnings so far.
        print("Pooled Cards: " + str(pooled_cards))
        print("Round Winner: Player #" + str(round_winner[0]))

        # Give the winner all the pooled cards.
        for card in pooled_cards:
            # Indexed/key'd the player using the round_winner ID.
            player_list[round_winner[0]].get_cd().append(card)

        #print("Remaining Players: " + str(len(player_list)))

        round_counter += 1
        round_winner.clear() # Empty it between every round.
        pooled_cards.clear()
    
    # Should only print once for the last remaining player.
    for player in player_list.values():
        print("### GAME OVER ###")
        print("Player #" + str(player.get_id()) + " is the winner of Card Battle Royale!")

        # Should total up to 12 * num_players.
        print("They have collected all " + str(len(player.get_bd()) + len(player.get_cd()) + len(player.get_hand())) + " cards!")
    return

def main() -> None:
    
    # Determines if the user wants player vs AI or have a simulated AI vs AI
    game_mode = acquire_game_mode()

    # Prompts user for # of playersbo to setup the game.
    num_bots = acquire_bots(game_mode)

    # Generates the deck based on # of players + shuffles it.
    if game_mode == 1:
        total_players = num_bots + 1 # Plus the user themself.
    elif game_mode == 2:
        total_players = num_bots
    
    # Determines if we are doing top-deck or strategic.
    ai_style = []
    ai_type = acquire_ai_type()

    # Top-deck(1), then there is no AI choice pattern.
    if ai_type == 1:
        for i in range(total_players):
            ai_style.append(1)
    # Strategic, we allocate them as Random(2) or Highest Value(3) then.
    elif ai_type == 2:
        for i in range(total_players):
            ai_style.append(random.randint(2,3))

    game_deck = create_deck(total_players)
    
    # Split the deck into equal parts for the players.
    split_deck = numpy.array_split(game_deck, total_players)

    # Initialize a dictionary containing all players, we Key them with their IDs.
    player_list = {}

    # Give them their decks as well. User player will be player_list[1].
    for i in range(total_players):
        if game_mode == 1 and i == 0: # Init the user player specifically for a bot_ai of "None"
            player_list[i+1] = Player(i+1, split_deck[i].tolist(), None) 
        else: # Else init all bots
            player_list[i+1] = Player(i+1, split_deck[i].tolist(), ai_style[i]) 

    """If you want to check what AI each bot has to check if their decisions are correct."""
    #for player in player_list.values():
        #print("Player #" + str(player.get_id()) + "'s AI is " + player.get_ai())

    # Begin running the battle simulation.
    start_simulation(player_list)
    return
main()
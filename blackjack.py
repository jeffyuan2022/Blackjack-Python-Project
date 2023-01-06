from deck import Deck
from hand import DealerHand, PlayerHand
from card import Card

# don't change these imports
from numpy.random import randint, seed
seed(20)

class Blackjack:
    """
    Game of blackjack!

    # Removes the game summaries from the previous doctest run
    >>> from os import remove, listdir
    >>> for f in listdir("game_summaries"):
    ...    remove("game_summaries/" + f)

    #######################################
    ### Doctests for calculate_score() ####
    #######################################
    >>> card_1 = Card("A", "diamonds")
    >>> card_2 = Card("J", "spades")
    >>> hand_1 = PlayerHand()
    >>> Blackjack.calculate_score(hand_1)
    0
    >>> hand_1.add_card(card_1)
    >>> Blackjack.calculate_score(hand_1) # (Ace)
    11
    >>> hand_1.add_card(card_2)
    >>> Blackjack.calculate_score(hand_1) # (Ace, Jack)
    21

    >>> card_3 = Card("A", "spades")
    >>> hand_2 = PlayerHand()
    >>> hand_2.add_card(card_1, card_3)
    >>> Blackjack.calculate_score(hand_2) # (Ace, Ace)
    12
    >>> hand_2.add_card(card_2)
    >>> Blackjack.calculate_score(hand_2) # (Ace, Ace, Jack)
    12

    >>> hand_3 = PlayerHand()
    >>> card_4 = Card(2, "spades")
    >>> card_5 = Card(4, "spades")
    >>> hand_3.add_card(card_4, card_5)
    >>> Blackjack.calculate_score(hand_3)
    6

    #######################################
    ### Doctests for determine_winner() ####
    #######################################
    >>> blackjack = Blackjack(10)
    >>> blackjack.determine_winner(10, 12)
    -1
    >>> blackjack.determine_winner(21, 21)
    0
    >>> blackjack.determine_winner(22, 23)
    0
    >>> blackjack.determine_winner(12, 2)
    1
    >>> blackjack.determine_winner(22, 2)
    -1
    >>> blackjack.determine_winner(2, 22)
    1
    >>> print(blackjack.get_log())
    Player lost with a score of 10. Dealer won with a score of 12.
    Player and Dealer tie.
    Player and Dealer tie.
    Player won with a score of 12. Dealer lost with a score of 2.
    Player lost with a score of 22. Dealer won with a score of 2.
    Player won with a score of 2. Dealer lost with a score of 22.
    <BLANKLINE>  
    >>> blackjack.reset_log()

    #######################################
    ### Doctests for play_round() #########
    #######################################
    >>> blackjack_2 = Blackjack(10)
    >>> blackjack_2.play_round(1, 15)
    >>> print(blackjack_2.get_log())
    Round 1 of Blackjack!
    wallet: 10
    bet: 5
    Player Cards: (10, clubs) (A, clubs)
    Dealer Cards: (Q, clubs) (?, ?)
    Dealer Cards Revealed: (7, diamonds) (Q, clubs)
    Player won with a score of 21. Dealer lost with a score of 17.
    <BLANKLINE>
    >>> blackjack_2.reset_log()
   
    >>> blackjack_2.play_round(3, 21)
    >>> print(blackjack_2.get_log())
    Round 2 of Blackjack!
    wallet: 15
    bet: 5
    Player Cards: (4, clubs) (7, clubs)
    Dealer Cards: (A, hearts) (?, ?)
    Player pulled a (J, hearts)
    Dealer Cards Revealed: (5, clubs) (A, hearts)
    Dealer pulled a (6, clubs)
    Dealer pulled a (2, clubs)
    Dealer pulled a (8, clubs)
    Player won with a score of 21. Dealer lost with a score of 22.
    Round 3 of Blackjack!
    wallet: 20
    bet: 10
    Player Cards: (6, hearts) (9, diamonds)
    Dealer Cards: (K, hearts) (?, ?)
    Player pulled a (Q, hearts)
    Dealer Cards Revealed: (J, diamonds) (K, hearts)
    Player lost with a score of 25. Dealer won with a score of 20.
    Round 4 of Blackjack!
    wallet: 10
    bet: 5
    Player Cards: (5, diamonds) (10, diamonds)
    Dealer Cards: (2, diamonds) (?, ?)
    Player pulled a (3, diamonds)
    Player pulled a (7, spades)
    Dealer Cards Revealed: (2, diamonds) (2, hearts)
    Dealer pulled a (K, spades)
    Dealer pulled a (3, spades)
    Player lost with a score of 25. Dealer won with a score of 17.
    <BLANKLINE>
    
    >>> with open("game_summaries/game_summary2.txt", encoding = 'utf-8') as f:
    ...     lines = f.readlines()
    ...     print("".join(lines[10:26]))
    Dealer Hand:
    ____
    |7  |
    | ♦ |
    |__7|
    ____
    |Q  |
    | ♣ |
    |__Q|
    Winner of ROUND 1: Player
    <BLANKLINE>
    ROUND 2:
    Player Hand:
    ____
    |4  |
    | ♣ |
    <BLANKLINE>

    >>> blackjack_3 = Blackjack(5)
    >>> blackjack_3.play_round(5, 21)
    >>> print(blackjack_3.get_log())
    Round 1 of Blackjack!
    wallet: 5
    bet: 5
    Player Cards: (2, clubs) (2, hearts)
    Dealer Cards: (2, diamonds) (?, ?)
    Player pulled a (3, clubs)
    Player pulled a (3, diamonds)
    Player pulled a (3, hearts)
    Player pulled a (3, spades)
    Player pulled a (4, clubs)
    Player pulled a (4, diamonds)
    Dealer Cards Revealed: (2, diamonds) (2, spades)
    Dealer pulled a (4, hearts)
    Dealer pulled a (4, spades)
    Dealer pulled a (5, clubs)
    Player lost with a score of 24. Dealer won with a score of 17.
    Wallet amount $0 is less than bet amount $5.

    >>> blackjack_4 = Blackjack(500)
    >>> blackjack_4.play_round(13, 21) # At least 52 cards will be dealt
    >>> blackjack_4.reset_log()
    >>> blackjack_4.play_round(1, 17)
    >>> print(blackjack_4.get_log())
    Not enough cards for a game.
    """
    # Class Attribute(s)
    class_counter = 0

    def __init__(self, wallet):
        # Initialize instance attributes
        # auto-increment as needed
        self.deck = Deck()
        self.wallet = wallet
        Blackjack.class_counter += 1
        self.num_games = Blackjack.class_counter #need check
        self.log = "" #need check
        self.round = 0
    
    def play_round(self, num_rounds, stand_threshold):
        """
        Plays `num_rounds` Blackjack rounds.

        Parameters:
            num_rounds (int): Number of rounds to play.
            stand_threshold (int): Score threshold for when the player
            will stand (ie player stands if they have a score >= 
            this threshold)
        """
        # This could get pretty long!
        assert isinstance(num_rounds, int)
        assert num_rounds>=0
        assert isinstance(stand_threshold, int)
        bet_amount = 5
        for i in range(num_rounds):
            self.player = PlayerHand()
            self.dealer = DealerHand()
            self.round += 1
            
            if len(self.deck.get_cards()) < 4: # 1
                self.log += "Not enough cards for a game."
                break
            if self.wallet < bet_amount: # 2
                self.log += "Wallet amount ${} is less than bet amount ${}.".format(self.wallet, bet_amount)
                break
            
            self.log += "Round {} of Blackjack!\n".format(self.round)
            self.log += "wallet: {}\n".format(self.wallet)
            self.log += "bet: {}\n".format(bet_amount)

            self.deck.shuffle(mongean=randint(6), modified_overhand=randint(6)) # 3

            self.deck.deal_hand(self.player) # 4
            self.deck.deal_hand(self.dealer)
            self.deck.deal_hand(self.player)
            self.deck.deal_hand(self.dealer)

            self.log += "Player Cards: {} {}\n".format(repr(self.player.cards[0]), repr(self.player.cards[1])) # 5
            self.log += "Dealer Cards: {} {}\n".format(repr(self.dealer.cards[0]), repr(self.dealer.cards[1]))

            self.hit_or_stand(self.player, stand_threshold) # 6

            self.dealer.reveal_hand() # 7
            self.log += "Dealer Cards Revealed: {} {}\n".format(repr(self.dealer.cards[0]), repr(self.dealer.cards[1]))

            self.hit_or_stand(self.dealer, 17) # 8

            result = self.determine_winner(Blackjack.calculate_score(self.player), Blackjack.calculate_score(self.dealer)) # 9
            if result == 1:
                self.wallet += bet_amount
                bet_amount += 5
            elif result == -1:
                self.wallet -= bet_amount
                if bet_amount > 5:
                    bet_amount -= 5

            self.add_to_file(self.player, self.dealer, result) # 10

            
    def calculate_score(hand):
        """
        Calculates the score of a given hand. 

        Sums up the ranks of each card in a hand. Jacks, Queens, and Kings
        have a value of 10 and Aces have a value of 1 or 11. The value of each
        Ace card is dependent on which value would bring the score closer
        (but not over) 21. 

        Should be solved using list comprehension and map/filter. No explicit
        for loops.

        Parameters:
            hand: The hand to calculate the score of.
        Returns:
            The best score as an integer value.
        """
        assert isinstance(hand, PlayerHand) or (isinstance(hand, DealerHand))
        value_lst = ["J", "Q", "K"]
        rank = [card.rank for card in hand.cards]
        num_lst_ace = len([i for i in rank if i=="A"])
        sum_hand = sum([10 if i in value_lst else 1 if i =="A" else i for i in rank])
        updated_sum = [sum_hand + i*10 for i in range(num_lst_ace+1)]
        close_21 = list(filter(lambda x: x<=21, updated_sum))
        if sum_hand > 21:
            return sum_hand
        else:
            return max(close_21)

    def determine_winner(self, player_score, dealer_score):
        """
        Determine whether the Blackjack round ended with a tie, dealer winning, 
        or player winning. Update the log to include the winner and
        their scores before returning.

        Returns:
            1 if the player won, 0 if it is a tie, and -1 if the dealer won
        """
        if (player_score > dealer_score and player_score <= 21) or (player_score <= 21 and dealer_score > 21):
            self.log +="Player won with a score of " + str(player_score)+ ". Dealer lost with a score of " + str(dealer_score)+ ".\n"
            return 1
        elif player_score == dealer_score or (player_score > 21 and dealer_score > 21):
            self.log +="Player and Dealer tie.\n"
            return 0
        else:
            self.log +="Player lost with a score of " + str(player_score)+ ". Dealer won with a score of " + str(dealer_score)+ ".\n"
            return -1



    def hit_or_stand(self, hand, stand_threshold):
        """
        Deals cards to hand until the hand score has reached or surpassed
        the `stand_threshold`. Updates the log everytime a card is pulled.

        Parameters:
            hand: The hand the deal the cards to depending on its score.
            stand_threshold: Score threshold for when the player
            will stand (ie player stands if they have a score >= 
            this threshold).
        """
        score = Blackjack.calculate_score(hand)
        if isinstance(hand, DealerHand) == True:
            Name = "Dealer"
        else:
            Name = "Player"
        while score < stand_threshold and len(self.deck.get_cards()) > 0:
            self.log += "{} pulled a {}\n".format(Name, repr(self.deck.get_cards()[0]))
            self.deck.deal_hand(hand)
            score = Blackjack.calculate_score(hand)



    def get_log(self):
        return self.log
    
    def reset_log(self):
        self.log = ""
        
        
    def add_to_file(self, player_hand, dealer_hand, result):
        """
        Writes the summary and outcome of a round of Blackjack to the 
        corresponding .txt file. This file should be named game_summaryX.txt 
        where X is the game number and it should be in `game_summaries` 
        directory.
        """
        
        # Remember to use encoding = "utf-8" 
        with open("./game_summaries/game_summary{}.txt".format(self.num_games), 'a+', encoding = "utf-8") as f:
            f.write("ROUND {}:\n".format(self.round))
            f.write("Player Hand:\n")
            f.write(str(player_hand))
            f.write("\nDealer Hand:\n")
            f.write(str(dealer_hand))
            if result == 1:
                Winner = "Player"
            elif result == -1:
                Winner = "Dealer"
            elif result == 0:
                Winner = "Tied"
            f.write("\nWinner of ROUND {}: {}\n\n".format(self.round, Winner))
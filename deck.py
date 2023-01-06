from card import Card
from hand import PlayerHand, DealerHand
from shuffle import Shuffle

class Deck:
    """
    Card deck of 52 cards.

    >>> deck = Deck()
    >>> deck.get_cards()[:5]
    [(2, clubs), (2, diamonds), (2, hearts), (2, spades), (3, clubs)]

    >>> deck.shuffle(modified_overhand=2, mongean=3)
    >>> deck.get_cards()[:5]
    [(A, clubs), (Q, clubs), (10, clubs), (7, diamonds), (5, diamonds)]

    >>> hand = PlayerHand()
    >>> deck.deal_hand(hand)
    >>> deck.get_cards()[0]
    (Q, clubs)
    """

    # Class Attribute(s)

    def __init__(self):
        """
        Creates a Deck instance containing cards sorted in ascending order.
        """
        self.cards = sorted([Card(rank, suit) for rank in Card.rank_sorted for suit in Card.suit_sorted])

    def shuffle(self, **shuffle_and_count):
        """Shuffles the deck using a variety of different shuffles.

        Parameters:
            shuffle_and_count: keyword arguments containing the
            shuffle type and the number of times the shuffled
            should be called.
        """
        shuffle_type = ["modified_overhand", "mongean"]
        assert all([i in shuffle_type for i, num in shuffle_and_count.items()])
        assert all([isinstance(num, int) for suffle_type, num in shuffle_and_count.items()])
        assert all([num>=0 for suffle_type, num in shuffle_and_count.items()])
        lst = []
        for type,num in shuffle_and_count.items():
            lst.append((type, num))
            lst = sorted(lst)
        for tup in lst:
            if tup[0] == "modified_overhand":
                self.cards = Shuffle.modified_overhand(self.cards, tup[1])
            else:
                for i in range(tup[1]):
                    self.cards = Shuffle.mongean(self.cards)

    def deal_hand(self, hand):
        """
        Takes the first card from the deck and adds it to `hand`.
        """
        assert isinstance(hand, DealerHand) or (isinstance(hand, PlayerHand))
        hand.add_card(self.cards[0]) #need testing
        self.cards = self.cards[1:]

    def get_cards(self):
        return self.cards
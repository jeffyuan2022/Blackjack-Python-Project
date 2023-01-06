class Shuffle:
    """
    Different kinds of shuffling techniques.
    
    >>> cards = [i for i in range(52)]
    >>> cards[25]
    25
    >>> mod_oh = Shuffle.modified_overhand(cards, 1)
    >>> mod_oh[0]
    25
    >>> mod_oh[25] 
    24
 
    >>> mongean_shuffle = Shuffle.mongean(mod_oh)
    >>> mongean_shuffle[0]
    51
    >>> mongean_shuffle[26]
    25

    """    
        
    def modified_overhand(cards, num):
        assert isinstance(num, int)
        assert num>=0
        if num == 0:
            return cards
        else:
            bot_pick_cards = num // 2
            top_pick_cards = num - bot_pick_cards
           
            if num % 2 != 0 and len(cards) % 2 == 0: # num is odd and cards is even
                top_half = cards[:len(cards)//2]
                bot_half = cards[len(cards)//2:]
                new_card = top_half[-top_pick_cards:] + bot_half[:bot_pick_cards] + top_half[:-top_pick_cards] + bot_half[bot_pick_cards:]
                return Shuffle.modified_overhand(new_card, num - 1)
                   
            elif num % 2 == 0 and len(cards) % 2 != 0: # num is even and cards is odd
                top_half = cards[:len(cards)//2]
                bot_half = cards[len(cards)//2:]
                new_card = top_half[-top_pick_cards:] + bot_half[:bot_pick_cards] + top_half[:-top_pick_cards] + bot_half[bot_pick_cards:]
                return Shuffle.modified_overhand(new_card, num - 1)
           
            elif num % 2 == 0 and len(cards) % 2 == 0: # num is even and cards is even
                top_half = cards[:len(cards)//2]
                bot_half = cards[len(cards)//2:]
                new_card = top_half[-top_pick_cards:] + bot_half[:bot_pick_cards] + top_half[:-top_pick_cards] + bot_half[bot_pick_cards:]
                return Shuffle.modified_overhand(new_card, num - 1)
           
            elif num % 2 != 0 and len(cards) % 2 != 0: # num is odd and cards is odd
                top_half = cards[:len(cards)//2 + 1]
                bot_half = cards[len(cards)//2 + 1:]
                new_card = top_half[-top_pick_cards:] + bot_half[:bot_pick_cards] + top_half[:-top_pick_cards] + bot_half[bot_pick_cards:]
                return Shuffle.modified_overhand(new_card, num - 1)
                        
    def mongean(cards):
        if len(cards) == 0:
            return []
        else:
            if len(cards) % 2 == 0:
                return [cards[-1]] + Shuffle.mongean(cards[:-1])
            else:
                return Shuffle.mongean(cards[:-1]) + [cards[-1]]
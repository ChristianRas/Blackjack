from termcolor import colored
import random as r


class Card:
    
    """Card object that is represented by a suit ('heart', 'club', etc.), and a cardsymbol ('10', 'J', etc.)."""
    
    def __init__(self, suit, cardsymbol) -> None:
        
        cardsymbol_to_value_dictionary = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
    
        self.suit : str = suit
        self.cardsymbol : str = cardsymbol
        self.value : int = cardsymbol_to_value_dictionary[self.cardsymbol]
        
    def __str__(self) -> str:
        #print card with emoji for suit and colored numbers for red cards
        
        suit_emoji_dictionary = {"heart": "\u2665", "diamond": "\u2666", "spade": "\u2660", "club": "\u2663"}
        
        if self.suit in ["heart", "diamond"]:
            return f"{colored(f"{self.cardsymbol}", "red")}{suit_emoji_dictionary[self.suit]}"
        else:
            return f"{self.cardsymbol}{suit_emoji_dictionary[self.suit]}"

class Deck:
    
    """Container class for Card objects, initialised with 6 shuffled card decks."""
    
    def __init__(self) -> None:
        
        self.cards = []
        for _ in range(6):
            for suit in ["heart", "diamond", "spade", "club"]:
                for cardsymbol in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                    self.cards.append(Card(suit, cardsymbol))
        r.shuffle(self.cards)
        
    def show(self, number_of_cards_to_print: int=False) -> str:
        if number_of_cards_to_print is False:
            # print full deck
            for card in self.cards:
                print(card, end=" ")
        else:
            for i in range(number_of_cards_to_print):
                print(self.cards[i], end=" ")
        return ""
    
    def draw(self) -> Card:
        return self.cards.pop(0)
    
    
class PlayerHand:
    
    """container class for Card objects"""
    
    def __init__(self, cards: list[Card]|None = None) -> None:
        if cards == None:
            self.cards : list[Card] = []
        else:
            self.cards = cards
        self.virgin = True  # if the hand has two cards only (e.g. no hits or double down have been used)
        self.active = True  # If the hand is still in play (neither stood on or busted)
        self.value = False
    
    
    def __add__(self, card) -> None:
        self.cards.append(card)
        self.value = self.compute_hand_value()
        
        
    def show(self, handnumber=1) -> None:
        print(f"Player Hand {handnumber}: ", end="")
        for card in self.cards:
            print(card, end=" ")
        print(f"({self.compute_hand_value()})\n")
        return None
        
        
    def compute_hand_value(self) -> int:
        
        hand_value = 0
        for card in self.cards:
            hand_value += card.value
        
        # correct Aces from 11 to 1 if needed and possible
        if hand_value > 21:
            
            aces_found = [card.cardsymbol for card in self.cards].count("A")
            
            for i in range(aces_found):
                hand_value -= 10
                if hand_value <= 21:
                    break
        
        return hand_value
    
    
class DealerHand(PlayerHand):
    
    """container class for Card objects"""
    
    def __init__(self):
        super().__init__()
        self.soft = False
        
    def compute_hand_value(self) -> int:
        
        
        hand_value = 0
        
        if self.virgin:
            hand_value = self.cards[0].value
            
        else:
        
            for card in self.cards:
                hand_value += card.value
            
            # correct Aces from 11 to 1 if needed and update soft status of dealerhand
            number_of_corrections = 0
            if hand_value > 21:
                
                aces_found = [card.cardsymbol for card in self.cards].count("A")
                
                for i in range(aces_found):
                    hand_value -= 10
                    number_of_corrections += 1
                    if hand_value <= 21:
                        break
            
            if number_of_corrections < self.cards.count("A"):
                self.soft = True
            else:
                self.soft = False
        
        return hand_value
    
    
    def show(self):
        
        if self.virgin:
            
            print("Dealer Hand: ", self.cards[0], f"X ({self.compute_hand_value()})\n")
            
        else:
            
            print("Dealer Hand:", *self.cards, f"({self.compute_hand_value()})\n")
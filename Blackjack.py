from termcolor import colored
import random as r
import time
import os

cardsymbol_to_value_dictionary = {"a": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}

class Card:
    
    """Card object that is represented by a suit ('heart', 'club', etc.), a cardsymbol ('10', 'J', etc.) and a corresponding Blackjack card value (1-11)."""
    
    def __init__(self, suit, cardsymbol) -> None:
        
        self.suit : str = suit
        self.cardsymbol : str = cardsymbol
        self.value : int = cardsymbol_to_value_dictionary[cardsymbol]
        
    def __str__(self) -> str:
        
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
        
    def show(self, num: int=False) -> str:
        if num is False:
            for card in self.cards:
                print(card, end=" ")
        else:
            for i in range(num):
                print(self.cards[i], end=" ")
        return ""
    
    def draw(self) -> Card:
        return self.cards.pop(0)
    
class PlayerHand:
    
    """container class for Card objects"""
    
    def __init__(self) -> None:
        self.cards : list[Card] = []
        self.virgin = True  # if the hand has two cards only (or for the case of DealerHand weather dealer is hiding second card)
        self.active = True  # If the hand it not stood on or busted
        self.soft = False  # for DealerHand if hand is soft or hard
    
    def __add__(self, card) -> None:
        self.cards.append(card)
        self.value()  # update potential aces that gets converted to a value of 1
        
    def show(self, handnumber=1) -> None:
        print(f"Player Hand {handnumber}: ", end="")
        for card in self.cards:
            print(card, end=" ")
        print(f"({self.value()})\n")
        return None
        
    def value(self) -> int:
        
        while True:
            value = 0
            for card in self.cards:
                value += card.value
            
            if value > 21 and any(card.cardsymbol == "A" for card in self.cards):
                next_card = next(card for card in self.cards if card.cardsymbol == "A")
                next_card.cardsymbol = "a"
                next_card.value = 1
            else:
                break
        
        return value
    
class DealerHand(PlayerHand):
    
    """container class for Card objects"""
    
    def show(self):
        if self.virgin:
            print(f"Dealer Hand: {self.cards[0]} X ({self.cards[0].value})\n")
        else:
            print(f"Dealer Hand: ", end="")
            for card in self.cards:
                print(card, end=" ")
                
            print(f"({self.value()})\n")
            
    def __add__(self, card) -> None:
        self.cards.append(card)
        if self.virgin:  #TODO check this works
            pass
        else:
            self.value()  # update potential aces that gets converted to a value of 1
                
    
def clear_screen() -> None:
    os.system("cls")
        
def print_money(amount: float, loss=False) -> str:
    if not loss:
        return colored(f"{amount}$", "green")
    else:
        return colored(f"{amount}$", "red")

def menu_select(options: list) -> int:
    
    """Promts user to select choise from ordered list of options i.e. [option1, option2, ...].
    User selects the option by entering 1-len(options) and that value is returend"""
    
    print("Select action:")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
        
    is_int = False
    in_range = False
    
    while not (is_int and in_range):
        
        is_int = False
        in_range = False
        selection = input()
        
        try:
            selection = int(selection)
            is_int = True
        except ValueError:
            print("Please enter valid number")
            continue
        
        if 0 < selection <= len(options):
            in_range = True
        else:
            print("Please select valid option")
            continue
        
    print("")
    return selection

def showhands(player_hands: list, dealerhand: DealerHand) -> None:
    dealerhand.show()
    for i in range(len(player_hands)):
        player_hands[i].show(handnumber=i+1)


def evaluate_game(playerhand: PlayerHand, dealerhand: DealerHand) -> float:
    
    """Evaluates ONE playerhand against the dealers and returns the payout ratio"""
    
    payout_ratio = 0
    
    if playerhand.value() > 21:
        print(f"Player busts\n")
        return payout_ratio
    elif dealerhand.value() > 21:
        print(f"Dealer busts\n")
        
        if playerhand.value() == 21:
            print("Player has Blackjack!")
            time.sleep(1)
            payout_ratio = 4
        else:
            payout_ratio = 2.5
            
        return payout_ratio
    elif playerhand.value() == dealerhand.value():
        print("Draw!\n")
        payout_ratio = 1
        return payout_ratio
    elif playerhand.value() == 21:
        print("Blackjack!\n")
        payout_ratio = 4
        return payout_ratio
    elif playerhand.value() > dealerhand.value():
        print("Player beats dealer\n")
        payout_ratio  =2.5
        return payout_ratio
    else:
        print("Dealer beats player\n")
        return payout_ratio
    

def main():
    
    """Runs a blackjack simulation with sidebets of Perfect Pairs and 21+3 and options for double down and split.
       The Payout Ratios have been increased to make it a winning game, it is for fun after all."""
    
    def evaluate_sidebets(playerhand: PlayerHand, dealerhand: DealerHand):
        
        # TODO test all sidebets with working examples
        nonlocal balance
        playercard_1 = playerhand.cards[0]
        playercard_2 = playerhand.cards[1]
        dealercard = dealerhand.cards[0]
        
        
        print("Evaluating sidebets...\n")
        time.sleep(2)
        
        # Perfect Pairs
        perfect_pair = (playercard_1.cardsymbol.upper() == playercard_2.cardsymbol.upper()) and (playercard_1.suit == playercard_2.suit)
        coloured_pair = (playercard_1.cardsymbol.upper() == playercard_2.cardsymbol.upper()) and (
            (playercard_1.suit in ["heart", "diamond"] and playercard_2.suit in ["heart", "diamond"]) or (playercard_1.suit in ["club", "spade"] and playercard_2.suit in ["club", "spade"])
            ) and not perfect_pair
        mixed_pair = (playercard_1.cardsymbol.upper() == playercard_2.cardsymbol.upper()) and not (perfect_pair or coloured_pair)
        
        perfect_pairs_payout_ratio = 0
        
        if perfect_pair:
            print("Player has a Perfect Pair!\n")
            perfect_pairs_payout_ratio = 50
            time.sleep(1)
        elif coloured_pair:
            print("Player has a coloured pair!\n")
            time.sleep(1)
            perfect_pairs_payout_ratio = 15
        elif mixed_pair:
            print("Player has a mixed pair\n")
            perfect_pairs_payout_ratio = 5
            time.sleep(1)
        else:
            pass
        
        if perfect_pairs_payout_ratio > 0:
            print(f"Player wins {print_money(perfect_pairs_payout_ratio*10)}\n")
            balance += perfect_pairs_payout_ratio*10  #TODO this throws UnboundLocalError...
            time.sleep(3)
        else:
            pass
        
        # 21+3
        twentyone_plus_three_payout_ratio = 0
        ranks = [cardsymbol_to_value_dictionary[card.cardsymbol] for card in [playercard_1, playercard_2, dealercard]]
        ranks.sort()
        flush = playercard_1.suit == playercard_2.suit == dealercard.suit
        straight = (ranks[0] + 2 == ranks[1] + 1 == ranks[2]) or (ranks == [2, 3, 14])
        three_of_a_kind = playercard_1.cardsymbol.upper() == playercard_2.cardsymbol.upper() == dealercard.cardsymbol.upper()
        straight_flush = straight and flush
        suited_three_of_a_kind = flush and three_of_a_kind
        
        if suited_three_of_a_kind:
            print("Player has Suited Three Of a Kind!\n")
            twentyone_plus_three_payout_ratio = 100
            time.sleep(1)
        elif straight_flush:
            print("Player has a Straight Flush!\n")
            twentyone_plus_three_payout_ratio = 50
            time.sleep(1)
        elif three_of_a_kind:
            print("Player has Three Of a Kind!\n")
            twentyone_plus_three_payout_ratio = 40
            time.sleep(1)
        elif straight:
            print("Player has a straight\n")
            twentyone_plus_three_payout_ratio = 15
            time.sleep(1)
        elif flush:
            print("Player has a Flush\n")
            twentyone_plus_three_payout_ratio = 10
            time.sleep(1)
        
        if twentyone_plus_three_payout_ratio > 0:
            print(f"Player wins {print_money(twentyone_plus_three_payout_ratio*10)}\n")
            balance += twentyone_plus_three_payout_ratio*10
            time.sleep(3)
        else:
            pass
        
        if (perfect_pairs_payout_ratio == 0) and (twentyone_plus_three_payout_ratio==0):
            print("Player loses on sidebets\n")
            time.sleep(2)
        
    
    balance = 1000
    blackjack_bets = [0]
    game_started = False
    
    clear_screen()
    print("\nHello, and welcome to BlackJack!\n")
    time.sleep(1)
    
    while balance >= 120:
        clear_screen()
        
        print(f"Your balance is {print_money(balance)}\n\n")
        if not game_started:
            play_selection = menu_select(["Play", "Quit"])
        else:
            play_selection = 1
        
        if play_selection == 2:
            break
        
        elif play_selection == 1:
            
            blackjack_bets = [100]
            balance -= 120
            deck = Deck()
            player_hands = [PlayerHand()]
            dealerhand = DealerHand()
            
            print("Placing bets...\n")
            time.sleep(1)
            clear_screen()
            print(f"Your balance is {print_money(balance)}\n\n")
            print("Placing bets...\n")
            print(f"Bets are:\nPerfect Pairs: {print_money(10)}\nBlackjack: {print_money(100)}\n21+3: {print_money(10)}\n")
            time.sleep(2)
            clear_screen()
            print("Dealing cards...\n")
            time.sleep(1)
                
            for _ in range(2):
                player_hands[0] + deck.draw()
                dealerhand + deck.draw()
            
            active_hand = ""
            
            # sidebets
            clear_screen()
                
            showhands(player_hands, dealerhand)
            
            evaluate_sidebets(player_hands[0], dealerhand)  #TODO consider adding continue promt here
            
            if player_hands[0].value() == 21:
                active_hand = player_hands[0].active = False
            else:
                # Player turn
                while True:  # Player turn
                
                    clear_screen()
                    
                    showhands(player_hands, dealerhand)
                    
                    active_hand = next((hand for hand in player_hands if hand.active is True), None)
                    if active_hand is not None:
                        active_hand_index = player_hands.index(active_hand)
                    
                    if active_hand is None:
                        break
                    else:            
                    
                        player_game_options = ["Hit", "Stand"]
                        
                        if active_hand.virgin:  #TODO add check if money in balance is enough?
                            player_game_options.append("Double Down")
                            
                            if active_hand.cards[0].cardsymbol == active_hand.cards[1].cardsymbol:
                                player_game_options.append("Split")
                        else:
                            pass
                        
                        print(f"Active hand is Player Hand {player_hands.index(active_hand)+1}\n")
                        player_game_selection = menu_select(player_game_options)
                        
                        if player_game_selection == 1:
                            print("Player hits...\n")
                            active_hand + deck.draw()
                            if active_hand.value() >= 21:
                                active_hand.active = False
                            else:
                                active_hand.virgin = False
                                
                        elif player_game_selection == 2:
                            print("Player stands...\n")
                            active_hand.active = False
                            
                        elif player_game_selection == 3:
                            print("Player doubles down...\n")
                            time.sleep(2)
                            
                            balance -= blackjack_bets[active_hand_index]
                            blackjack_bets[active_hand_index] *= 2
                            
                            print(f"New bets are:")
                            for i in range(len(blackjack_bets)):
                                print(f"Hand {i+1} bet: {print_money(blackjack_bets[i])}")
                            print("")
                            time.sleep(2)
                            
                            print("Player draws...\n")
                            
                            active_hand + deck.draw()
                            active_hand.active = False
                            
                        elif player_game_selection == 4:
                            print("Player splits...\n")
                            time.sleep(2)
                            
                            balance -= blackjack_bets[active_hand_index]
                            blackjack_bets.insert(active_hand_index+1, blackjack_bets[active_hand_index])
                            print(f"New balance is {print_money(balance)}\n")
                            time.sleep(1)
                            
                            print(f"New bets are:")
                            for i in range(len(blackjack_bets)):
                                print(f"Hand {i+1} bet: {print_money(blackjack_bets[i])}")
                            print("")
                            time.sleep(2)
                            
                            print("Player draws...\n")
                            
                            temporary_hand_1 = PlayerHand()
                            temporary_hand_2 = PlayerHand()
                            
                            temporary_hand_1 + active_hand.cards[0]
                            temporary_hand_1 + deck.draw()
                            temporary_hand_2 + active_hand.cards[1]
                            temporary_hand_2 + deck.draw()
                            
                            player_hands[active_hand_index] = temporary_hand_1
                            player_hands.insert(active_hand_index + 1, temporary_hand_2)
                            
                        time.sleep(2)
                    
            if all(hand.value() > 21 for hand in player_hands):
                pass
            else:
                # Dealer turn
                clear_screen()
                showhands(player_hands, dealerhand)
                time.sleep(2)
                
                clear_screen()
                showhands(player_hands, dealerhand)
                print("Dealer Shows...\n")
                time.sleep(2)
            
                dealerhand.virgin = False    
                clear_screen()
                showhands(player_hands, dealerhand)
                
                while True:
                    
                    clear_screen()
                    showhands(player_hands, dealerhand)
                
                    if any(card.cardsymbol == "A" for card in dealerhand.cards):
                        dealerhand.soft = True
                    
                    if (dealerhand.value() < 17 and dealerhand.soft is False) or (dealerhand.value() <= 17 and dealerhand.soft is True):
                        time.sleep(2)
                        print("Dealer hits...")
                        dealerhand + deck.draw()
                        time.sleep(2)
                    else:
                        time.sleep(2)
                        print("Dealer Stands...")
                        time.sleep(2)
                        break
            
            # Conluding game
            
            clear_screen()
            showhands(player_hands, dealerhand)
            
            time.sleep(1)
            total_earnings = 0
            for i in range(len(player_hands)):
                print(f"Evaluating hand {i+1}...\n")
                
                time.sleep(2)
                
                payout_ratio = evaluate_game(player_hands[i], dealerhand)
                
                time.sleep(2)
                
                if payout_ratio > 0:
                    print(f"Player wins {print_money(payout_ratio*blackjack_bets[i])}\n")
                    balance += payout_ratio*blackjack_bets[i]
                    total_earnings += payout_ratio*blackjack_bets[i]
                else:
                    print(f"Player loses {print_money(blackjack_bets[i], loss=True)}\n")
                    total_earnings -= blackjack_bets[i]
                time.sleep(1)
                    
            
            
            if (len(player_hands) > 1) and (total_earnings > 0):
                time.sleep(1)
                print(f"Total money earned: {print_money(total_earnings)}\n")
            elif (len(player_hands) > 1) and (total_earnings < 0):
                time.sleep(1)
                print(f"Total money lost {print_money(total_earnings, loss=True)}")
            else:
                pass
            
            time.sleep(2)
            
        continue_game_selection = menu_select(["Play again", "Quit"])
        
        if continue_game_selection == 1:
            game_started = True
        elif continue_game_selection == 2:
            break
                        
if __name__ == "__main__":
    main()


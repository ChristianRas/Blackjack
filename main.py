from termcolor import colored
import time
import os
from BlackjackCardModule import Card, Deck, PlayerHand, DealerHand

    
def clear_screen() -> None:
    os.system("cls")
        
        
def print_money(amount: float, loss=False) -> str:
    if not loss:
        return colored(f"{amount}$", "green")
    else:
        return colored(f"{amount}$", "red")


def menu_select(options: list) -> int:
    
    # Promts user to select index (using 1-index) from ordered list of options i.e. [option1, option2, ...]
    
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
    
    if playerhand.compute_hand_value() > 21:
        print(f"Player busts\n")
        return payout_ratio
    elif dealerhand.compute_hand_value() > 21:
        print(f"Dealer busts\n")
        
        if playerhand.compute_hand_value() == 21:
            print("Player has Blackjack!\n")
            payout_ratio = 3.5
        else:
            payout_ratio = 2.5
            
        return payout_ratio
    elif playerhand.compute_hand_value() == dealerhand.compute_hand_value():
        print("Draw!\n")
        payout_ratio = 1
        return payout_ratio
    elif playerhand.compute_hand_value() == 21:
        print("Blackjack!\n")
        payout_ratio = 4
        return payout_ratio
    elif playerhand.compute_hand_value() > dealerhand.compute_hand_value():
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
        
        nonlocal balance
        
        playercard_1 = playerhand.cards[0]
        playercard_2 = playerhand.cards[1]
        dealercard = dealerhand.cards[0]
        
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
            time.sleep(0.5)
        elif coloured_pair:
            print("Player has a coloured pair!\n")
            time.sleep(0.5)
            perfect_pairs_payout_ratio = 15
        elif mixed_pair:
            print("Player has a mixed pair\n")
            perfect_pairs_payout_ratio = 5
            time.sleep(0.5)
        else:
            pass
        
        if perfect_pairs_payout_ratio > 0:
            print(f"Player wins {print_money(perfect_pairs_payout_ratio*10)}\n")
            balance += perfect_pairs_payout_ratio*10
            time.sleep(1)
        else:
            pass
        
        # 21+3
        twentyone_plus_three_payout_ratio = 0
        cardsymbol_to_value_dictionary = {"a": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}   
        ranks = [list(cardsymbol_to_value_dictionary).index(card.cardsymbol.upper()) + 1 for card in [playercard_1, playercard_2, dealercard]]
        ranks.sort()
        flush = playercard_1.suit == playercard_2.suit == dealercard.suit
        straight = (ranks[0] + 2 == ranks[1] + 1 == ranks[2]) or (ranks == [2, 3, 14])
        three_of_a_kind = playercard_1.cardsymbol.upper() == playercard_2.cardsymbol.upper() == dealercard.cardsymbol.upper()
        straight_flush = straight and flush
        suited_three_of_a_kind = flush and three_of_a_kind
        
        if suited_three_of_a_kind:
            print("Player has Suited Three Of a Kind!\n")
            twentyone_plus_three_payout_ratio = 100
            time.sleep(0.5)
        elif straight_flush:
            print("Player has a Straight Flush!\n")
            twentyone_plus_three_payout_ratio = 50
            time.sleep(0.5)
        elif three_of_a_kind:
            print("Player has Three of a Kind!\n")
            twentyone_plus_three_payout_ratio = 40
            time.sleep(0.5)
        elif straight:
            print("Player has a Straight\n")
            twentyone_plus_three_payout_ratio = 15
            time.sleep(0.5)
        elif flush:
            print("Player has a Flush\n")
            twentyone_plus_three_payout_ratio = 10
            time.sleep(0.5)
        
        if twentyone_plus_three_payout_ratio > 0:
            print(f"Player wins {print_money(twentyone_plus_three_payout_ratio*10)}\n")
            balance += twentyone_plus_three_payout_ratio*10
            time.sleep(0.5)
        else:
            pass
        
        if (perfect_pairs_payout_ratio == 0) and (twentyone_plus_three_payout_ratio==0):
            print("Player loses on sidebets\n")
        
        menu_select(["Continue"])
    
        
    current_directory = os.path.dirname(os.path.abspath(__file__))
    balance_file_path = os.path.join(current_directory, 'balance.txt')
    
    try:
        balance_file = open(balance_file_path, "r")
        balance = float(balance_file.readline())
        print(f"Read balance is {balance}")
        balance_file.close()
    except FileNotFoundError:
        balance = 1000
    
    blackjack_bets = [0]
    initial_load = True
    
    clear_screen()
    print("\nHello, and welcome to BlackJack!\n")
    time.sleep(1)
    
    while balance >= 120:
        clear_screen()
        
        print(f"Your balance is {print_money(balance)}\n\n")
        if initial_load:
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
            print(f"Bets are:\nPerfect Pairs: {print_money(10)}\nBlackjack: {print_money(100)}\n21+3: {print_money(10)}\n")
            time.sleep(1)
            clear_screen()
            print("Dealing cards...\n")
            time.sleep(1)
                
            for _ in range(2):
                player_hands[0] + deck.draw()
                dealerhand + deck.draw()
            
            """
            For testing
            =============================================
            player_hands[0].cards[0] = Card("heart", "2")
            player_hands[0].cards[1] = Card("spade", "A")
            dealerhand.cards[0] = Card("diamond", "2")
            dealerhand.cards[1] = Card("heart", "7")
            deck.cards[0] = Card("spade", "K")
            """
            
            clear_screen()
            showhands(player_hands, dealerhand)
            time.sleep(1)
            
            evaluate_sidebets(player_hands[0], dealerhand)

            while True:  # Player turn
            
                clear_screen()
                showhands(player_hands, dealerhand)
                
                active_hand = next((hand for hand in player_hands if hand.active is True), None)
                
                if active_hand is None:
                    break
                
                else:
                    
                    active_hand_index = player_hands.index(active_hand)
                    
                    if active_hand.compute_hand_value() > 21:
                        active_hand.active = False
                        print(f"Player busts on hand {active_hand_index+1}!")
                        time.sleep(1)
                        continue
                    
                    if active_hand.compute_hand_value() == 21:
                        print(f"Player stands on hand {active_hand_index+1}")
                        active_hand.active = False
                        time.sleep(1)
                        continue
                
                    player_game_options = ["Hit", "Stand"]
                    
                    if balance >= blackjack_bets[active_hand_index]:  #check if its possible to do further betting
                        
                        if active_hand.virgin:
                            player_game_options.append("Double Down")
                            
                        if active_hand.cards[0].value == active_hand.cards[1].value:
                            player_game_options.append("Split")
                        
                    
                    print(f"Active hand is Player Hand {active_hand_index+1}\n")
                    player_game_selection = menu_select(player_game_options)
                    
                    if player_game_selection == 1:
                        active_hand + deck.draw()
                        active_hand.virgin = False
                            
                    elif player_game_selection == 2:
                        active_hand.active = False
                        
                    elif player_game_selection == 3:
                        balance -= blackjack_bets[active_hand_index]
                        blackjack_bets[active_hand_index] *= 2
                        active_hand + deck.draw()
                        active_hand.active = False
                        
                    elif player_game_selection == 4:
                        
                        balance -= blackjack_bets[active_hand_index]
                        blackjack_bets.insert(active_hand_index+1, blackjack_bets[active_hand_index])
                        
                        cards_to_split = active_hand.cards[0], active_hand.cards[1]
                        
                        player_hands[active_hand_index] = PlayerHand([cards_to_split[0], deck.draw()])
                        player_hands.insert(active_hand_index + 1, PlayerHand([cards_to_split[1], deck.draw()]))
                        
            
                    
            if all(hand.compute_hand_value() > 21 for hand in player_hands):
                pass  #skip dealer action
            else:
                # Dealer turn
                
                clear_screen()
                showhands(player_hands, dealerhand)
                time.sleep(1)
                print("Dealer Shows...\n")
                time.sleep(1)
            
                dealerhand.virgin = False
                
                while True:
                    
                    clear_screen()
                    showhands(player_hands, dealerhand)
                    
                    if (dealerhand.compute_hand_value() < 17 and dealerhand.soft is False) or (dealerhand.compute_hand_value() <= 17 and dealerhand.soft is True):
                        time.sleep(1)
                        print("Dealer hits...")
                        dealerhand + deck.draw()
                        time.sleep(1)
                        
                    else:
                        
                        time.sleep(1)
                        print("Dealer Stands...")
                        time.sleep(1)

                        break
            
            # Conluding game
            clear_screen()
            showhands(player_hands, dealerhand)
            total_won = 0
            for i in range(len(player_hands)):
                print(f"Evaluating hand {i+1}...\n")
                time.sleep(0.5)
                
                payout_ratio = evaluate_game(player_hands[i], dealerhand)
                time.sleep(0.5)
                
                if payout_ratio > 0:
                    payout = payout_ratio * blackjack_bets[i]
                    print(f"Player wins {print_money(payout - 100)}\n")
                    balance += payout
                    total_won += payout - 100
                else:
                    print(f"Player loses {print_money(blackjack_bets[i], loss=True)}\n")
                    total_won -= blackjack_bets[i]
            
            if (len(player_hands) > 1) and (total_won > 0):
                print(f"Total money earned: {print_money(total_won)}\n")
            elif (len(player_hands) > 1) and (total_won < 0):
                print(f"Total money lost {print_money(total_won, loss=True)}")
            else:
                pass
            
        continue_game_selection = menu_select(["Play again", "Quit"])
        
        if continue_game_selection == 1:
            initial_load = False
        elif continue_game_selection == 2:
            break

    if balance <= 120:  # don't trigger if user simply quit
        print("Oh no you are broke!")
        
    balance_file = open(balance_file_path, "w")
    if balance >= 120:
        balance_file.write(str(balance))
    else:
        balance_file.write(str(1000))
    balance_file.close()

if __name__ == "__main__":
    main()

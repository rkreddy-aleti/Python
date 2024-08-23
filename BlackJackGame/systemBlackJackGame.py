import os
import random
from art import logo


def clean_screen():
    """Clear the screen and Print the BlackJack's logo"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)


def deal_cards():
    """Select a card from 12 pack of cards."""
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    # Select a random card and return the card value.
    card = random.choice(cards)
    return card


def sum_of_cards(cards):
    """Sum all the card values and return the sum of all collected cards """
    total = 0

    for card in cards:
        if card == "A":
            total += 11
        elif card in ["J", "Q", "K"]:
            total += 10
        else:
            total += int(card)

    return total


def calculate_score(cards):
    """Calculate and return the sum of collected cards"""
    score = sum_of_cards(cards)

    if score == 21 and len(cards) == 2:
        return 0
    
    if "A" in cards and score > 21:
        score -= 10
    
    return score


def compare_scores(user_score, computer_score):
    """Compare the user score with computer score and return the Winner of game."""
    if user_score == computer_score:
        return "Match draw 🙃 and You can also try one more time.", "draw"
    elif user_score == 0:
        return "You win with a BlackJack 😎", "user"
    elif computer_score == 0:
        return "You lose with Computer's BlackJack 😱", "computer"
    elif user_score > 21:
        return "You went over and lose 😭", "computer"
    elif computer_score > 21:
        return "Computer went over and You win 😁", "user"
    elif user_score > computer_score:
        return "Wow... You win 😃", "user"
    else:
        return "Ohh... You lose 😤", "computer"

    
def play_game():
    """Actual game starts here"""
    # intiation of the packs and scores
    user_cards = []
    user_score = -1
    computer_cards = []
    computer_score = -1
    is_game_over = False

    # pick the first and second cards from the pack.
    for card in range(2):
        user_cards.append(deal_cards())
        computer_cards.append(deal_cards())
    
    while not is_game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
    
        print(f"Your cards: {user_cards}, current score: {user_score}")
        print(f"Computer's first card: {computer_cards[0]}\n")

        if user_score == 0 or computer_score == 0 or user_score > 21:
            is_game_over = True

        elif user_score == 21:
            is_game_over = True

        else:
            play_next = input(f"Type 'y' to get another card, type 'n' to pass: ")
            if play_next == "y":
                user_cards.append(deal_cards())
            else:
                is_game_over = True
        
    while computer_score != 0 and computer_score < 17 and user_score <= 21:
        computer_cards.append(deal_cards())
        computer_score = calculate_score(computer_cards)
    
    computer_score = calculate_score(computer_cards)
    print(f"\nYour final hand: {user_cards} and final score: {user_score}")
    print(f"Computer's final hand: {computer_cards} and final score: {computer_score}")
    x, y = compare_scores(user_score, computer_score)
    print(x)
    return y


def bet_calculate(balance):
    """Calculate the bet amount based on the coins avialable."""
    bank_balance = balance
    bet = 0
    coins = [1,2,5,10,20,50,100,200,500,1000,5000]
    continue_bet = True

    while bet < bank_balance and continue_bet:
        print(f"\nThe avialable coins for bet: {coins}")
        selected_coin = input("Enter the Coin (or type \"D for done\"): ").lower()
        if selected_coin == "d":
            continue_bet = False
            break
        elif selected_coin.isdigit():
            selected_coin = int(selected_coin)
            if selected_coin in coins:        
                if selected_coin > bank_balance:
                    print("You have placed a Bigger coin than your balance, please a smaller coin.\n")

                else:
                    valid_bet = True
                    while valid_bet:
                        no_of_coins = input("How many coins do you want to place: ")
                        if no_of_coins.isdigit():
                            bet_amount = selected_coin * int(no_of_coins)
                            bet += bet_amount
                            if bet > bank_balance:
                                print("\nYou have placed more coins than you balance, please place lesser coins.")
                                bet -= bet_amount
                            else:
                                valid_bet = False
                        else:
                            print("You have entered wrong input.")

                print(f"The bet amount till now: {bet}")
            
        else:
            print("You have placed the wrong coin, please place the proper coin.\n")

    clean_screen()
    return bet


def game_start(balance):
    """Here, you have entered into gaming zonw with Bank balance."""
    bank_balance = balance

    print(f"\nYou Bank balance: {bank_balance}")
    bet = bet_calculate(bank_balance)
    print(f"\nYou Bank balance: {bank_balance}")
    print(f"\nThe final bet amount is: {bet}")
    
    if bank_balance >= bet and bet > 0:
        # Enter into the game...
        winner = play_game()
        if winner == "user":
            bank_balance += bet
        elif winner == "computer":
            bank_balance -= bet
    
        # print(f"\nYou Bank balance: {bank_balance}")

    else:
        print("You have entered wrong bet, please try again less than your bank balance.")
        bank_balance = game_start(bank_balance)
    
    return bank_balance, bet


def determine_level(total_bet, rounds_played, default_amount):
    """Determine the difficulty level based on the total bet amount and the number of rounds played."""

    if total_bet <= 2 * default_amount and rounds_played < 2:
        level = "Beginner"

    elif 2 * default_amount < total_bet <= 5 * default_amount and 2 <= rounds_played < 5:
        level = "Medium"

    elif total_bet > 10 * default_amount and rounds_played >= 1:
        level = "Expert"
    else:
        # Edge cases that don't fit exactly in the above categories
        if total_bet > 10 * default_amount or rounds_played > 10:
            level = "Expert"
        elif total_bet > 5 * default_amount or rounds_played >= 5:
            level = "Medium"
        else:
            level = "Beginner"
    
    print("\n====================== SUMMARY OF THE THIS GAME ======================")
    if level == "Expert":
        print(f"\nWow, You are an Expert. \nTotal bet you have placed: {total_bet}\nTotal rounds played: {rounds_played}")
    elif level == "Medium":
        print(f"\nNice, You are at Medium. \nTotal bet you have placed: {total_bet}\nTotal rounds played: {rounds_played}")
    else:
        print(f"\nSad, You are just Beginner. \nTotal bet you have placed: {total_bet}\nTotal rounds played: {rounds_played}")


# Program execution starts from here by clearing the screen.
clean_screen()

default_amount = 100
bank_balance = default_amount
total_bet = 0
no_of_games = 0

while bank_balance >= 0:
   

    if bank_balance == 0:
        determine_level(total_bet, no_of_games, default_amount)
        continue_game = input("\nYou have lost the complete bank balance,\nDo you want to restart the game with the default balance? (\"y\" or \"n\"): ").lower()
        if continue_game == "y":
            total_bet = 0
            no_of_games = 0
            bank_balance = default_amount
            clean_screen()
            bank_balance, bet = game_start(bank_balance)
            total_bet += bet            

        else:
            break

    print(f"\nYou Bank balance: {bank_balance}")
    play = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower()
    no_of_games += 1

    if play == 'y':
        clean_screen()
        bank_balance, bet = game_start(bank_balance)
        total_bet += bet

    elif play == 'n':
        break

    else:
        clean_screen()
        print("You have entered wrong input 😏, please try again.")

print(f"\nYou can play this game at anytime by executing this program.\nThank you...😍")

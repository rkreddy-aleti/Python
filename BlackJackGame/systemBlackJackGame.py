import os
import random
from typing import List, Tuple

# try to import ascii art logo; fall back to simple text if not available
try:
    from art import logo  # type: ignore
except Exception:
    logo = "=== BLACKJACK ==="


def clean_screen() -> None:
    """Clear the screen and print the Blackjack logo (if available)."""
    os.system("cls" if os.name == "nt" else "clear")
    print(logo)


def deal_cards() -> str:
    """Select a card from a pack and return its symbol."""
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    return random.choice(cards)


def sum_of_cards(cards: List[str]) -> int:
    """
    Convert card symbols to a numeric total treating A as 11 initially.
    J/Q/K = 10, numeric strings converted to int.
    """
    total = 0
    for card in cards:
        if card in ("J", "Q", "K"):
            total += 10
        elif card == "A":
            total += 11
        else:
            try:
                total += int(card)
            except Exception:
                total += 0
    return total


def calculate_score(cards: List[str]) -> int:
    """
    Calculate and return the blackjack score.
    Return 0 as special code for a natural blackjack (two-card 21).
    """
    score = sum_of_cards(cards)

    # Natural blackjack: two cards that total 21 (e.g., A + 10-value)
    if score == 21 and len(cards) == 2:
        return 0

    # If over 21 and there is an Ace counted as 11, convert A(11) to A(1) by subtracting 10
    ace_count = cards.count("A")
    while score > 21 and ace_count:
        score -= 10
        ace_count -= 1

    return score


def compare_scores(user_score: int, computer_score: int) -> Tuple[str, str]:
    """
    Compare user and dealer scores and return (message, winner).
    winner is one of: "user", "computer", "draw"
    """
    if user_score == computer_score:
        return ("Draw 🙃 — No one wins.", "draw")
    if user_score == 0:
        return ("Blackjack! You win 🥳", "user")
    if computer_score == 0:
        return ("Opponent has Blackjack. You lose 😭", "computer")
    if user_score > 21:
        return ("You went over. You lose 😭", "computer")
    if computer_score > 21:
        return ("Opponent went over. You win 🎉", "user")
    if user_score > computer_score:
        return ("You win 🎉", "user")
    return ("You lose 😭", "computer")


def play_game() -> str:
    """
    A simple non-interactive round used for testing.
    Returns 'user'|'computer'|'draw'.
    """
    user_cards: List[str] = [deal_cards(), deal_cards()]
    computer_cards: List[str] = [deal_cards(), deal_cards()]

    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    # dealer plays if needed
    while computer_score != 0 and computer_score < 17 and user_score <= 21:
        computer_cards.append(deal_cards())
        computer_score = calculate_score(computer_cards)

    _, winner = compare_scores(user_score, computer_score)
    return winner


def bet_calculate(balance: int) -> int:
    """
    Console helper to assemble a bet by adding coins.
    Returns final bet amount.
    """
    coins = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 5000]
    bet = 0
    while True:
        clean_screen()
        print(f"Current balance: ${balance}")
        print(f"Current bet: ${bet}")
        print("Available coins:", ", ".join(map(str, coins)))
        print("Enter coin value to add, or 'd' when done, or 'q' to cancel:")
        choice = input("> ").strip().lower()
        if choice == "d":
            break
        if choice == "q":
            bet = 0
            break
        try:
            coin = int(choice)
            if coin not in coins:
                print("Invalid coin. Press Enter to continue.")
                input()
                continue
            count = input("How many of this coin? (enter integer): ").strip()
            count_i = int(count) if count else 1
            addition = coin * max(1, count_i)
            if bet + addition > balance:
                print("Bet would exceed balance. Press Enter to continue.")
                input()
                continue
            bet += addition
        except Exception:
            print("Invalid input. Press Enter to continue.")
            input()
    clean_screen()
    return bet


def game_start(balance: int) -> Tuple[int, int]:
    """
    Console-driven game start that asks for bet and plays a single round.
    Returns (new_balance, bet)
    """
    bank_balance = balance
    print(f"\nYour Bank balance: {bank_balance}")
    bet = bet_calculate(bank_balance)
    print(f"\nFinal bet amount: {bet}")
    if bet <= 0 or bet > bank_balance:
        print("No valid bet placed. Returning to menu.")
        return bank_balance, 0

    # subtract stake
    bank_balance -= bet

    # deal
    user_cards = [deal_cards(), deal_cards()]
    computer_cards = [deal_cards(), deal_cards()]

    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    # player loop
    while user_score != 0 and user_score <= 21:
        print(f"\nYour cards: {user_cards}, current score: {user_score}")
        print(f"Computer's first card: {computer_cards[0]}")
        move = input("Type 'h' to hit, 's' to stand: ").strip().lower()
        if move == "h":
            user_cards.append(deal_cards())
            user_score = calculate_score(user_cards)
            if user_score > 21:
                break
        elif move == "s":
            break

    # dealer plays
    while computer_score != 0 and computer_score < 17 and user_score <= 21:
        computer_cards.append(deal_cards())
        computer_score = calculate_score(computer_cards)

    print(f"\nYour final hand: {user_cards} final score: {user_score}")
    print(f"Computer's final hand: {computer_cards} final score: {computer_score}")
    message, winner = compare_scores(user_score, computer_score)
    print(message)

    # settle
    if winner == "user":
        bank_balance += bet * 2
    elif winner == "draw":
        bank_balance += bet

    return bank_balance, bet


def determine_level(total_bet: int, rounds_played: int, default_amount: int) -> None:
    """
    Print a simple summary / level suggestion based on betting and rounds.
    """
    print("\n====================== SUMMARY OF THIS GAME ======================")
    print(f"Starting balance: ${default_amount}")
    print(f"Rounds played: {rounds_played}")
    print(f"Total bet amount: ${total_bet}")

    if total_bet <= 2 * default_amount and rounds_played < 2:
        print("Level: Beginner — low betting activity.")
    elif 2 * default_amount < total_bet <= 5 * default_amount and 2 <= rounds_played < 5:
        print("Level: Intermediate — moderate betting activity.")
    elif total_bet > 10 * default_amount and rounds_played >= 1:
        print("Level: High Roller — large betting activity.")
    else:
        # Edge cases that don't fit exactly in the above categories
        if total_bet > 10 * default_amount or rounds_played > 10:
            print("Level: Expert — very high betting activity.")
        elif total_bet > 5 * default_amount or rounds_played >= 5:
            print("Level: Medium — above average betting activity.")
        else:
            print("Level: Beginner — low betting activity.")


# Only run the console main loop when executed directly.
if __name__ == "__main__":
    # Program execution starts from here by clearing the screen.
    clean_screen()

    default_amount = 100
    bank_balance = default_amount
    total_bet = 0
    no_of_games = 0

    while bank_balance >= 0:
        if bank_balance == 0:
            determine_level(total_bet, no_of_games, default_amount)
            continue_game = input(
                "\nYou have lost the complete bank balance,\nDo you want to restart the game with the default balance? (\"y\" or \"n\"): "
            ).lower()
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

        if play == "y":
            clean_screen()
            bank_balance, bet = game_start(bank_balance)
            total_bet += bet
        elif play == "n":
            break
        else:
            clean_screen()
            print("You have entered wrong input 😏, please try again.")

    print(f"\nYou can play this game at anytime by executing this program.\nThank you...😍")

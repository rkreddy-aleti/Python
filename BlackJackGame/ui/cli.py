import sys
import os

# make sure parent package/module is importable
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from systemBlackJackGame import clean_screen, game_start

def main_menu():
    clean_screen()
    print("=== Blackjack CLI ===")
    balance = 100
    while True:
        print(f"\nCurrent bank balance: {balance}")
        cmd = input("Play a round? (y)es / (n)o / (q)uit: ").lower()
        if cmd == "y":
            clean_screen()
            balance, bet = game_start(balance)
        elif cmd == "n":
            print("Okay. Come back soon.")
        elif cmd == "q":
            break
        else:
            print("Unknown command. Use y, n, or q.")

if __name__ == "__main__":
    main_menu()
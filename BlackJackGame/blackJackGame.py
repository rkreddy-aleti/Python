import os
import random
from art import logo

# Clear the terminal screen
os.system('cls' if os.name == 'nt' else 'clear')
print(logo)


def continue_game(cards):
   #intiation of the packs and scores
    cards = cards
    your_cards = []
    your_score = 0
    computer_cards = []
    computer_score = 0

    if play == "y":
        
        # first card pick
        your_cards.append(random.choice(cards))
        computer_cards.append(random.choice(cards))

        # second card pick
        your_cards.append(random.choice(cards))
        computer_cards.append(random.choice(cards))
    
        your_score =sum(your_cards)
        computer_score = sum(computer_cards)
        
        print(f"Your cards: {your_cards}, current score: {your_score}")
        print(f"Computer's first card: {computer_cards[0]}\n")

        continue_play = True
        while continue_play:
            if your_score == 21:
                print(f"WoW... You got the JackPot.\nYou score: {your_score}.")
                computer_play = True
                while computer_play:
                    computer_score = sum(computer_cards)
                    if computer_score == 21:
                        print(f"Computer's cards: {computer_cards}\n")
                        print("Match draw 😁")
                        computer_play = False
                    elif computer_score < 21:
                        computer_cards.append(random.choice(cards))
                        print(f"Computer's cards: {computer_cards}, computer score: {computer_score}\n")
                    else:
                        print(f"Computer's cards: {computer_cards}, computer score: {computer_score}\n")
                        print(f"Your cards: {your_cards}, current score: {your_score}")
                        print("You win 😁")
                        computer_play = False 
                continue_play = False


            if your_score < 21:
                play_next = input(f"Type 'y' to get another card, type 'n' to pass: ")
                if play_next == "y":
                    your_cards.append(random.choice(cards))
                    your_score = sum(your_cards)
                    print(f"Your cards: {your_cards}, current score: {your_score}")
                    print(f"Computer's first card: {computer_cards[0]}\n")

                else:
                    computer_score = sum(computer_cards)
                    print(f"Computer's cards: {computer_cards}, computer score: {computer_score}\n")

                    computer_play = True
                    while computer_play:
                        if computer_score == 21:
                            print(f"Computer's cards: {computer_cards}\n")
                            print("You lose 😤")
                            computer_play = False
                            continue_play = False

                        elif computer_score < 21:
                            if computer_score > your_score:
                                print(f"Computer's cards: {computer_cards}\n")
                                print("You lose 😤")
                                computer_play = False
                                continue_play = False
                            else:
                                computer_cards.append(random.choice(cards))
                                computer_score = sum(computer_cards)
                                print(f"Computer's cards: {computer_cards}, computer score: {computer_score}\n")
                        else:
                            # print(f"Computer's cards: {computer_cards}, computer score: {computer_score}\n")
                            print(f"Your cards: {your_cards}, current score: {your_score}")
                            print("You win 😁")
                            computer_play = False
                            continue_play = False

            elif your_score > 21:
                print(f"Computer's cards: {computer_cards}, computer score: {computer_score}\n")
                print(f"Your cards: {your_cards}, current score: {your_score}")
                print("You lose 😤")
                continue_play = False

A = 1
J = 10
Q = 10
K = 10

cards = [A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K]
want_to_play = True

while want_to_play:
    play = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ")
    if play == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(logo)

        continue_game(cards)
    
    else:
     print("Thank you...😁")
     want_to_play = False

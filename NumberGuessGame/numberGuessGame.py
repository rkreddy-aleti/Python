from art import logo
import os

def clear_screen():
    """Clear the screen and Print the Number Guess game logo"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)

clear_screen()
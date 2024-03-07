#Rock, Paper, Scissors Game

def get_choices():
    player_choice = input("Enter a choice (rock,paper,scissors: )")
    computer_choice = "paper"
    choices = {"player" : player_choice,"computer":computer_choice}
    return choices

choices = get_choices()
print(choices)

#Data Storage with Dictionaries

import random 

def get_choices():
    player_choice = input("Enter a choice (rock,paper,scissors: )")
    options = ["rock","paper","scissors"]
    computer_choice = random.choice(options)
    choices = {"player" : player_choice,"computer":computer_choice}
    return choices

choices = get_choices()
print(choices)

food =["pizza","carrots","eggs"]
dinner = random.choice(food)

#RPS - Function Arguments

import random 

def get_choices():
    player_choice = input("Enter a choice (rock,paper,scissors: )")
    options = ["rock","paper","scissors"]
    computer_choice = random.choice(options)
    choices = {"player" : player_choice,"computer":computer_choice}
    return choices

def check_win(player,computer):
    #RPS - concatinating Strings
    print("you chose" + player + ",computer chose" + computer)

    #RPS -f-strings
    print(f"you chose {player},computer chose {computer}")

    #RPS - IF statement
    if player == computer:
        return "It's a tie!"
    elif player == "rock" and computer == "scissors":
        return "Rock smashes scissors! you Win!"
    elif player == "rock" and computer == "paper":
        return "paper covers rock! you lose."
    
    #RPS - nested-IF statement
    if player == computer:
        return "It's a tie!"
    elif player == "rock":
        if computer == "scissors":
            return "Rock smashes scissors! you Win!"
        else:
            return "paper covers rock! you lose."
    elif player == "paper":
        if computer == "rock":
            return "paper covers rock ! you Win!"
        else:
            return "scissors cuts paper! you lose."
    elif player == "scissors":
        if computer == "paper":
            return "scissors cuts paper! you Win!"
        else:
            return "rock smashes scissors! you lose."    
    
choices = get_choices()
result =check_win(choices["player"],choices["computer"])
print(result)

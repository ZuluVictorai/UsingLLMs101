#zack viola
#2t1
#code works 
#create a code where the user is asked to move forward, backwards, left or right. once the choice has been made, there is only one direction where they live, all other situations, the user dies.|
#code was then asked to make the correct answer random

import random
def play_game():
    directions = ["forward", "backward", "left", "right"]
    correct_direction = random.choice(directions)
    print("You are standing in the middle of a forest. You hear a distant growling sound behind you.")
    print("You have four options: move forward, move backward, move left, move right.")
    choice = input("Enter your choice (forward, backward, left, right): ")
    if choice.lower() == correct_direction:
        print(f"You chose to move {choice} and escaped the beast. You survived!")
    else:
        print(f"You chose the wrong direction and are lost in the forest. Game over!")
play_game()
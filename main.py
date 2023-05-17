# 1-7: Upgrades, 8-14: Traps
import os
import random
from race import Race, Car
from colorama import Fore

cards = {1: "V8 Engine", 2: "Carbon-fiber Chassis", 3: "Fix", 4: "Repair", 5: "Camera", 6: "Spare Parts", 7: "Asset",
         8: "Spikes", 9: "Weight", 10: "Explosive", 11: "Overheat", 12: "Reporter", 13: "Speed Limit", 14: "Liability"}
deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 2, 3, 4, 5, 6,
        8, 9, 10, 11, 12, 13]
random.shuffle(deck)
discard = []
turn = 1
hand1 = []  # P1's hand
hand2 = []  # P2's hand
power = False

# Shuffles deck when cards are done
def shuffle():
    global deck
    global discard
    if len(deck) == 0:
        deck = discard
        random.shuffle(deck)
        discard = []


# Draws a card for hand
def draw():
    global deck
    x = deck.pop()
    shuffle()
    check()
    return x

def draw_():
    global deck
    x = deck.pop()
    shuffle()
    return x

def view(player, camera):
    if player == 1:
        print("Here are your cards: " if not camera else "These are your opponent's cards:")
        if len(hand1) == 3:
            print("1." + cards[hand1[0]] + ", 2." + cards[hand1[1]] + ", 3." + cards[hand1[2]])
        else:
            print("1." + cards[hand1[0]] + ", 2." + cards[hand1[1]])
    else:
        print("Here are your cards: " if not camera else "These are your opponent's cards:")
        if len(hand2) == 3:
            print("1." + cards[hand2[0]] + ", 2." + cards[hand2[1]] + ", 3." + cards[hand2[2]])
        else:
            print("1." + cards[hand2[0]] + ", 2." + cards[hand2[1]])


def check1():
    for hand in hand1:
        if hand != 7 and hand != 14:
            return False
    return True


def check2():
    for hand in hand2:
        if hand != 7 and hand != 14:
            return False
    return True


def check():
    x = False
    while not x:
        if check1():
            discard.append(hand1.pop())
            hand1.append(draw_())
            x = False
        elif check2():
            discard.append(hand2.pop())
            hand2.append(draw_())
            x = False
        else:
            x = True


# Plays a card from hand
def play():
    global turn
    global power
    while True:
        view(turn % 2, False)
        choice = "0"
        while choice != "1" and choice != "2" and choice != "3":
            if turn % 2 == 1:
                choice = input("\nPlayer 1, what card do you want to play? (Select a number from 1-3): ")
            else:
                choice = input("\nPlayer 2, what card do you want to play? (Select a number from 1-3): ")
        global hand1
        global hand2
        if turn % 2 == 1:
            x = hand1.pop(int(choice) - 1)
            discard.append(x)
        else:
            x = hand2.pop(int(choice) - 1)
            discard.append(x)
        if x == 5:
            view(turn % 2 + 1, True)
        elif x == 6:
            view(turn % 2, False)
            y = "0"
            while y != "1" and y != "2":
                y = input("Discard one or both cards (Select a number from 1-2):")
            if y == "1":
                z = "0"
                while z != "1" and z != "2":
                    z = input("What card do you want to discard? (Select a number from 1-2): ")
                if turn % 2 == 1:
                    discard.append(hand1.pop(int(choice) - 1))
                    hand1.append(draw())
                else:
                    discard.append(hand2.pop(int(choice) - 1))
                    hand2.append(draw())
            else:
                if turn % 2 == 1:
                    hand1 = [draw(), draw()]
                else:
                    hand2 = [draw(), draw()]
        elif x == 12:
            if turn % 2 == 1:
                print(Fore.YELLOW + "You have removed " + str(
                    cards[hand2.pop(random.randint(0, 2))]) + " from your Opponent's hand." + Fore.WHITE)
                hand2.append(draw())
            else:
                print(Fore.YELLOW + "You have removed " + str(
                    cards[hand1.pop(random.randint(0, 2))]) + " from your Opponent's hand." + Fore.WHITE)
                hand1.append(draw())
        elif x == 7:
            if (turn % 2 == 1 and (hand1[0] > 6 or hand1[0] == 5) and (hand1[1] > 6 or hand1[1] == 5)) or (
                    turn % 2 == 0 and (hand2[0] > 6 or hand2[0] == 5) and (hand2[1] > 6 or hand2[1] == 5)):
                print("You don't have any upgrade cards to play the asset with.")
                if turn % 2 == 0:
                    hand2.append(7)
                else:
                    hand1.append(7)
                continue
            else:
                y = "0"
                while True:
                    while y != "1" and y != "2":
                        y = input("Choose an upgrade card (not camera) to play the asset with: (Pick 1 or 2):")
                    if (turn % 2 == 1 and (hand1[int(y) - 1] > 6 or hand1[int(y) - 1] == 5)) or (
                            turn % 2 == 0 and (hand2[int(y) - 1] > 6 or hand2[int(y) - 1] == 5)):
                        y = "0"
                        continue
                    break
                if turn % 2 == 1:
                    x = hand1.pop(int(y) - 1)
                    discard.append(x)
                    hand1.append(draw())
                else:
                    x = hand2.pop(int(y) - 1)
                    discard.append(x)
                    hand2.append(draw())
                power = True
                if x == 6:
                    print(Fore.YELLOW + "You got another turn with fresh cards!")
                    if turn % 2 == 1:
                        hand1 = [draw_(), draw_(), draw_()]
                        check()
                        continue
                    else:
                        hand2 = [draw_(), draw_(), draw_()]
                        check()
                        continue
        elif x == 14:
            if (turn % 2 == 1 and (hand1[0] < 8 or hand1[0] == 14) and (hand1[1] < 8 or hand1[1] == 14)) or (
                    turn % 2 == 0 and (hand2[0] < 8 or hand2[0] == 14) and (hand2[1] < 8 or hand2[1] == 14)):
                print("You don't have any trap cards to play the liability with.")
                if turn % 2 == 0:
                    hand2.append(14)
                else:
                    hand1.append(14)
                continue
            else:
                y = "0"
                while True:
                    while y != "1" and y != "2":
                        y = input("Choose a trap card to play the liability with: (Pick 1 or 2):")
                    if (turn % 2 == 1 and (hand1[int(y) - 1] < 8 or hand1[int(y) - 1] == 14)) or (
                            turn % 2 == 0 and (hand2[int(y) - 1] < 8 or hand2[int(y) - 1] == 14)):
                        y = "0"
                        continue
                    break
                if turn % 2 == 1:
                    x = hand1.pop(int(y) - 1)
                    discard.append(x)
                    hand1.append(draw_())
                else:
                    x = hand2.pop(int(y) - 1)
                    discard.append(x)
                    hand2.append(draw_())
                check()
                power = True
                if x == 12:
                    if turn % 2 == 1:
                        print(Fore.YELLOW + "You have removed " + str(
                            cards[hand2.pop(random.randint(0, 2))]) + " and " + str(
                            cards[hand2.pop(random.randint(0, 1))]) + " from your Opponent's hand." + Fore.WHITE)
                        hand2.append(draw_())
                        hand2.append(draw_())
                        check()
                    else:
                        print(Fore.YELLOW + "You have removed " + str(
                            cards[hand1.pop(random.randint(0, 2))]) + " and " + str(
                            cards[hand1.pop(random.randint(0, 1))]) + " from your Opponent's hand." + Fore.WHITE)
                        hand1.append(draw_())
                        hand1.append(draw_())
                        check()

        if turn % 2 == 1:
            hand1.append(draw())
        else:
            hand2.append(draw())
        turn += 1
        break
    return x


hand1 = [draw_(), draw_(), draw_()]

hand2 = [draw_(), draw_(), draw_()]
check()

p1 = Car()
p2 = Car()
race = Race(p1, p2)

#title
print(Fore.LIGHTBLUE_EX + '''
d8888b.  .d8b.   .o88b. d88888b       .d88b.  d88888b      d888888b db   db d88888b       d8888b. d8888b.  .d8b.  db   d8b   db 
88  `8D d8' `8b d8P  Y8 88'          .8P  Y8. 88'          `~~88~~' 88   88 88'           88  `8D 88  `8D d8' `8b 88   I8I   88 
88oobY' 88ooo88 8P      88ooooo      88    88 88ooo           88    88ooo88 88ooooo       88   88 88oobY' 88ooo88 88   I8I   88 
88`8b   88~~~88 8b      88~~~~~      88    88 88~~~           88    88~~~88 88~~~~~       88   88 88`8b   88~~~88 Y8   I8I   88 
88 `88. 88   88 Y8b  d8 88.          `8b  d8' 88              88    88   88 88.           88  .8D 88 `88. 88   88 `8b d8'8b d8' 
88   YD YP   YP  `Y88P' Y88888P       `Y88P'  YP              YP    YP   YP Y88888P       Y8888D' 88   YD YP   YP  `8b8' `8d8'  

#################################################################################################################################                                                                                                                                                                                                                                           
''')
# intro
print("This game should be run in a Python IDE. Do the following for correct gameplay:")
print("Change your IDE Console's run configurations to emulate the Terminal")
input("Press enter when you've finished reading: ")
os.system('cls')
print("Welcome to Race of the Draw!")
print("Each turn, you can play one of the 3 cards that you're dealt")
print("There are 2 types, Upgrade Cards--which buff you, and Trap Cards--which harm your opponent.")
print("At the beginning and end of each turn, you will see")
print("the progress your cars have made!\n")
print("Cars have two stats: Health and Speed. Speed lets you")
print("advance quicker on the track (0 speed means you're not")
print("moving), and if your health reaches 0, your car combusts")
print("and you lose!")
input("Press enter when you're finished reading: ")
os.system('cls')
print("Upgrade Cards:")
print("V8 Engine: +20 Speed")
print("Carbon-fiber Chassis: +30 Speed, -10 Health")
print("Fix: Removes DoT effects (i.e. removes Overheat and Spike)")
print("Repair: +20 Health")
print("Camera: See opponent's hand")
print("Spare Parts: Discard and draw one/both of remaining cards")
print("Asset: Played with any upgrade (except camera) to enhance it")
print("\n")
print("Trap Cards:")
print("Spikes: Opponent -45 Speed over 3 turns")
print("Weight: Opponent -20 Speed")
print("Explosive: Opponent -30 Health, but, 50% Chance for -10 Health to self")
print("Overheat: Opponent -45 Health over 3 turns")
print("Reporter: Removes a random card from opponent's hand (and allows you to see the discarded card)")
print("Speed Limit: Opponent -30 Speed if above a random limit, but 50% Chance for -10 Speed to self if you're also above the limit")
print("Liability: Played with any trap to enhance it")
print("\n")
input("Press enter when you're finished reading: ")
os.system('cls')
print("Each car starts with 100 health and 30 speed.")
print("Players win if the other player explodes (0 health) or if they cross the finish line!")
print("This is a passing game. Hand the computer to Player 1. When P1's turn is done, pass to")
print("P2, etc. until someone wins. Enjoy!")
input("Press enter when you're finished reading: " + Fore.WHITE)
os.system('cls')
while True:
    card = play()
    race.update_progress(turn - 1, card, power)
    power = False
    race.print_progress(turn)
    if race.has_p1_won() or race.has_p2_won():
        print('\n')
        race.print_progress(turn, False)
        break
    race.clear(turn)
    race.print_progress(turn + 1)

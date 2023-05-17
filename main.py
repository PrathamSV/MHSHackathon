# 1-7: Upgrades, 8-14: Traps
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
            hand1.append(draw())
            x = False
        elif check2():
            discard.append(hand2.pop())
            hand2.append(draw())
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
                print(Fore.YELLOW + "You have removed " + str(cards[hand2.pop(random.randint(0, 2))]) + " from your Opponent's hand." + Fore.WHITE)
                hand2.append(draw())
            else:
                print(Fore.YELLOW + "You have removed " + str(cards[hand1.pop(random.randint(0, 2))]) + " from your Opponent's hand." + Fore.WHITE)
                hand1.append(draw())
        elif x == 7:
            if (turn % 2 == 1 and (hand1[0] > 6 or hand1[0] == 5) and (hand1[0] > 6 or hand1[0] == 5)) or (turn % 2 == 0 and (hand2[0] > 6 or hand2[0] == 5) and (hand2[0] > 6 or hand2[0] == 5)):
                print("You don't have any upgrade cards to play the asset with.")
                if turn % 2 == 0:
                    hand2.append(7)
                else:
                    hand1.append(7)
                continue
            else:
                y = "0"
                while True:
                    while y != 1 and y != 2:
                        y = input("Choose an upgrade card (not camera) to play the asset with: (Pick 1 or 2):")
                    if (turn % 2 == 1 and (hand1[int(y) - 1] > 6 or hand1[int(y) - 1] == 5)) or (turn % 2 == 0 and (hand2[int(y) - 1] > 6 or hand2[int(y) - 1] == 5)):
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
                        hand1 = [draw(), draw(), draw()]
                        play()
                    else:
                        hand2 = [draw(), draw(), draw()]
                        play()
        elif x == 14:
            if (turn % 2 == 1 and (hand1[0] < 8 or hand1[0] == 14) and (hand1[0] < 8 or hand1[0] == 14)) or (turn % 2 == 0 and (hand2[0] < 8 or hand2[0] == 14) and (hand2[0] < 8 or hand2[0] == 14)):
                print("You don't have any trap cards to play the liability with.")
                if turn % 2 == 0:
                    hand2.append(14)
                else:
                    hand1.append(14)
                continue
            else:
                y = "0"
                while True:
                    while y != 1 and y != 2:
                        y = input("Choose a trap card to play the liability with: (Pick 1 or 2):")
                    if (turn % 2 == 1 and (hand1[int(y) - 1] < 8 or hand1[int(y) - 1] == 14)) or (turn % 2 == 0 and (hand2[int(y) - 1] < 8 or hand2[int(y) - 1] == 14)):
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
                if x == 12:
                    if turn % 2 == 1:
                        print(Fore.YELLOW + "You have removed " + str(
                            cards[hand1.pop(random.randint(0, 2))]) + " and " + str(
                            cards[hand1.pop(random.randint(0, 1))]) + " from your Opponent's hand." + Fore.WHITE)
                        hand2.append(draw())
                        hand2.append(draw())
                    else:
                        print(Fore.YELLOW + "You have removed " + str(
                            cards[hand2.pop(random.randint(0, 2))]) + " and " + str(
                            cards[hand2.pop(random.randint(0, 1))]) + " from your Opponent's hand." + Fore.WHITE)
                        hand1.append(draw())
                        hand1.append(draw())
                    
        if turn % 2 == 1:
            hand1.append(draw())
        else:
            hand2.append(draw())
        turn += 1
        break
    return x


for i in range(3):
    hand1.append(draw())
for i in range(3):
    hand2.append(draw())
check()
p1 = Car()
p2 = Car()
race = Race(p1, p2)
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

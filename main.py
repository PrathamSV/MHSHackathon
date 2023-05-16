# 1-7: Upgrades, 8-14: Traps
import random

cards = {1: "V8 Engine", 2: "Carbon-fiber Chassis", 3: "Fix", 4: "Repair", 5: "Camera", 6: "Spare Parts", 7: "Asset",
         8: "Spikes", 9: "Weight", 10: "Explosive", 11: "Overheat", 12: "Reporter", 13: "Speed Limit", 14: "Liability"}
deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 2, 3, 4, 5, 6,
        7, 8, 9, 10, 11, 12, 13, 14]
random.shuffle(deck)
discard = []
turn = 1
hand1 = []  # P1's hand
hand2 = []  # P2's hand


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
    return x


# Plays a card from hand
def play():
    choice = "0"
    while choice != "1" and choice != "2" and choice != "3":
        choice = input("What card do you want to play? (Select a number from 1-3): ")
    global hand1
    global hand2
    global turn
    x = 0
    if turn % 2 == 1:
        x = hand1.pop(int(choice))
        discard.append(x)
        hand1.append(draw())
    else:
        x = hand2.pop(int(choice))
        discard.append(x)
        hand2.append(draw())
    turn += 1
    return x


for i in range(3):
    hand1.append(draw())
for i in range(3):
    hand2.append(draw())
race = Race()
while True:
    card = play()
    race.update_progress(2 if turn % 2 == 0 else 1, card)
    if race.has_p1_won() or race.has_p2_won():
        break

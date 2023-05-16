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

# Plays a card from hand
def play():
    view(turn % 2, false)
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
    else:
        x = hand2.pop(int(choice))
        discard.append(x)
    turn += 1
    if x == 5:
         view(turn % 2 + 1, true)
    if x == 6:
         view(turn % 2, false)
         y = "0"
         while y != "1" and y != "2": input("Discard one or both cards (Select a number from 1-2):")
         if y == "1":
              z = "0"
              while z != "1" and z != "2": input("What card do you want to discard? (Select a number from 1-2): ")
              if turn % 2 == 1:
                  discard.append(hand1.pop(int(choice)))
                  hand1.append(draw())
              else:
                  discard.append(hand2.pop(int(choice)))
                  hand2.append(draw())
         else:
              if turn % 2 == 1:
                  hand1 = []
                  hand1.append(draw())
                  hand1.append(draw())
              else:
                  hand2 = []
                  hand2.append(draw())
                  hand2.append(draw())
    if turn % 2 == 1:
         hand1.append(draw())
    else:
         hand2.append(draw())
    return x


for i in range(3):
    hand1.append(draw())
for i in range(3):
    hand2.append(draw())
race = Race()
while True:
    card = play()
    race.update_progress(turn, card)
    if race.has_p1_won() or race.has_p2_won():
        break

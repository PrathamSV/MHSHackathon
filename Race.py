import random
from colorama import Fore

class Car:
    def __init__(self, speed=10, health=100):
        self.speed = speed
        self.health = health
        self.progress = 0
        self.sprite = 'CAR'
        self.is_spiked = [False, 0]
        self.is_overheated = [False, 0]

    def change_health(self, amount):
        self.health += self.health * (amount / 100)

    def change_speed(self, amount):
        self.speed += self.speed * (amount / 100)

    def update_progress(self):
        self.progress += int(self.speed / 10)
        if self.health <= 0:
            self.sprite = 'DED'
        return self.progress

    def spike(self):
        self.is_spiked = [True, 10]

    def overheat(self):
        self.is_overheated = [True, 3]





class Race:
    def __init__(self, p1: Car, p2: Car):
        self.p1 = p1
        self.p2 = p2
        self.call_dict = {1: V8, 2: chassis, 3: fix, 4: repair, 8: spikes, 9: hammer, 10: explosive, 11: overheat}

    def has_p1_won(self):
        if self.p2.health <= 0:
            print('p2 destroyed')
            return True
        if self.p1.progress >= 30:
            print('p1 crossed')
            return True
        return False

    def has_p2_won(self):
        if self.p1.health <= 0:
            print('p1 destroyed')
            return True
        if self.p2.progress >= 30:
            print('p2 crossed')
            return True
        return False

    def update_progress(self, turn, card=1):
        # spikes p1
        if self.p1.is_spiked[0]:
            self.p1.change_speed(-p1.is_spiked[1])
            if self.p1.is_spiked[1] >= 20:
                self.p1.is_spiked = [False, 0]
            else:
                self.p1.is_spiked[1] += 5

        # overheat p1
        if self.p1.is_overheated[0]:
            if self.p1.is_overheated[1] <= 0:
                self.p1.is_overheated = [False, 0]
            else:
                self.p1.change_speed(10)
                self.p1.is_overheated[1] -= 1

        # spikes p2
        if self.p2.is_spiked[0]:
            self.p2.change_speed(-p2.is_spiked[1])
            if self.p2.is_spiked[1] >= 20:
                self.p2.is_spiked = [False, 0]
            else:
                self.p2.is_spiked[1] += 5

        # overheat p2
        if self.p2.is_overheated[0]:
            if self.p2.is_overheated[1] <= 0:
                self.p2.is_overheated = [False, 0]
            else:
                self.p2.change_speed(10)
                self.p2.is_overheated[1] -= 1

        if turn % 2 == 1:
            # call card
            self.call_dict[card](1)
            # update
            self.p1.update_progress()
        if turn % 2 == 0:
            # call card
            self.call_dict[card](2)
            # update
            self.p2.update_progress()

    def print_progress(self):
        print(Fore.BLUE + "P1: " + (30 - p1.progress) * '_' + p1.sprite + (p1.progress * '_'))
        print(Fore.RED + "P2: " + (30 - p2.progress) * '_' + p2.sprite + (p2.progress * '_'))
        if self.has_p1_won():
            print(Fore.BLUE + "P1 WON!")
        if self.has_p2_won():
            print(Fore.RED + "P2 WON!")

        print(Fore.WHITE, end='')

    def V8(self, player):
        if player == 1:
            self.p1.change_speed(20)
        elif player == 2:
            self.p2.change_speed(20)

    def chassis(self, player):
        if player == 1:
            self.p1.change_speed(30)
            self.p1.change_health(-10)
        elif player == 2:
            self.p2.change_speed(30)
            self.p2.change_health(-10)

    def fix(self, player):
        if player == 1:
            self.p1.is_spiked = [False, 0]
            self.p1.is_overheated = [False, 0]
        elif player == 2:
            self.p2.is_spiked = [False, 0]
            self.p2.is_overheated = [False, 0]

    def repair(self, player):
        if player == 1:
            self.p1.change_health(20)
        elif player == 2:
            self.p2.change_health(20)

    def spikes(self, player):
        if player == 1:
            self.p2.spike()
        elif player == 2:
            self.p1.spike()

    def hammer(self, player):
        if player == 1:
            self.p2.change_health(-20)
        elif player == 2:
            self.p1.change_health(-20)

    def explosive(self, player):
        if player == 1:
            self.p2.change_health(-30)
            if random.choice([True, False]):
                self.p1.change_health(-10)
        if player == 2:
            self.p1.change_health(-30)
            if random.choice([True, False]):
                self.p2.change_health(-10)
                
    def overheat(self, player):
        if player == 1:
            self.p2.overheat()
        if player == 2:
            self.p1.overheat()
            

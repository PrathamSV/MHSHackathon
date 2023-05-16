import random
from colorama import Fore
import os


class Car:
    def __init__(self, speed: int = 30, health: int = 100) -> None:
        self.speed = speed
        self.health = health
        self.progress = 0
        self.sprite = 'CAR'
        self.is_spiked = [False, 0]
        self.is_overheated = [False, 0]

    def change_health(self, amount: int) -> None:
        if self.health + amount >= 0:
            self.health += amount
        else:
            self.health = 0

    def change_speed(self, amount: int) -> None:
        if self.speed + amount >= 0:
            self.speed += amount
        else:
            self.speed = 0

    def update_progress(self) -> int:
        self.progress += int(self.speed / 10)
        if self.health <= 0:
            self.sprite = 'DED'
        return self.progress

    # spike and overheat don't stack w/ themselves
    def spike(self) -> None:
        self.is_spiked = [True, 10]

    def overheat(self) -> None:
        self.is_overheated = [True, 3]


class Race:
    def v8(self, player: int) -> None:
        if player == 1:
            self.p1.change_speed(20)
        elif player == 2:
            self.p2.change_speed(20)
        print(Fore.YELLOW + "+20 Speed." + Fore.WHITE)

    def chassis(self, player: int) -> None:
        if player == 1:
            self.p1.change_speed(30)
            self.p1.change_health(-10)
        elif player == 2:
            self.p2.change_speed(30)
            self.p2.change_health(-10)
        print(Fore.YELLOW + "+30 Speed, -10 Health." + Fore.WHITE)

    def fix(self, player: int) -> None:
        if player == 1:
            self.p1.is_spiked = [False, 0]
            self.p1.is_overheated = [False, 0]
        elif player == 2:
            self.p2.is_spiked = [False, 0]
            self.p2.is_overheated = [False, 0]
        print(Fore.YELLOW + "All DoT effects removed." + Fore.WHITE)

    def repair(self, player: int) -> None:
        if player == 1:
            self.p1.change_health(20)
        elif player == 2:
            self.p2.change_health(20)
        print(Fore.YELLOW + "+20 Health." + Fore.WHITE)

    def spikes(self, player: int) -> None:
        if player == 1:
            self.p2.spike()
        elif player == 2:
            self.p1.spike()
        print(Fore.YELLOW + "Your opponent was spiked." + Fore.WHITE)

    def weight(self, player: int) -> None:
        if player == 1:
            self.p2.change_speed(-20)
        elif player == 2:
            self.p1.change_speed(-20)
        print(Fore.YELLOW + "Opponent -20 Speed." + Fore.WHITE)

    def explosive(self, player: int) -> None:
        did_self_dmg = False
        if player == 1:
            self.p2.change_health(-30)
            if random.choice([True, False]):
                self.p1.change_health(-10)
                did_self_dmg = True
        elif player == 2:
            self.p1.change_health(-30)
            if random.choice([True, False]):
                self.p2.change_health(-10)
                did_self_dmg = True

        if did_self_dmg:
            out = "Opponent -30 Health. But you damaged yourself in the process. Self -10 Health."
        else:
            out = "Opponent -30 Health."

        print(Fore.YELLOW + out + Fore.WHITE)

    def overheat(self, player: int) -> None:
        if player == 1:
            self.p2.overheat()
        elif player == 2:
            self.p1.overheat()
        print(Fore.YELLOW + "Opponent has Overheated." + Fore.WHITE)

    def speed_limit(self, player: int) -> None:
        self_got_caught = False
        opp_got_caught = False
        limit = random.randint(20, 80)
        print(Fore.YELLOW + "The speed limit is " + str(limit) + Fore.WHITE)

        if player == 1:
            if self.p2.speed >= limit:
                self.p2.change_speed(-30)
                opp_got_caught = True
            if self.p1.speed >= limit and random.choice([True, False]):
                self.p1.change_speed(-10)
                self_got_caught = True
        elif player == 2:
            if self.p1.speed >= limit:
                self.p1.change_speed(-30)
                opp_got_caught = True
            if self.p2.speed >= limit and random.choice([True, False]):
                self.p2.change_speed(-10)
                self_got_caught = True

        out = ""
        if opp_got_caught:
            out += "Your opponent was over the Speed Limit! Opp -30 Speed."
        if self_got_caught:
            out += "You were above the Speed Limit! Self -10 Speed."

        print(Fore.YELLOW + out + Fore.WHITE)

    def nothing(self, unused: int):  # do nothing
        pass

    def __init__(self, p1: Car, p2: Car) -> None:
        self.p1 = p1
        self.p2 = p2
        self.call_dict = {1: self.v8, 2: self.chassis, 3: self.fix, 4: self.repair, 5: self.nothing, 6: self.nothing,
                          7: self.nothing, 8: self.spikes, 9: self.weight, 10: self.explosive, 11: self.overheat,
                          12: self.nothing, 13: self.speed_limit, 14: self.nothing}

    def has_p1_won(self) -> bool:
        if self.p2.health <= 0:
            return True
        if self.p1.progress >= 30:
            return True
        return False

    def has_p2_won(self) -> bool:
        if self.p1.health <= 0:
            return True
        if self.p2.progress >= 30:
            return True
        return False

    def update_progress(self, turn: int, card: int) -> None:
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

        # spikes p1
        if self.p1.is_spiked[0]:
            self.p1.change_speed(-self.p1.is_spiked[1])
            print(Fore.YELLOW + "P1 is affected by Spikes. P1 " + str(-self.p1.is_spiked[1]) + " Speed" + Fore.WHITE)

            if self.p1.is_spiked[1] >= 20:
                self.p1.is_spiked = [False, 0]
                print(Fore.YELLOW + "P1 found a spare tire! P1 is no longer affected by Spikes" + Fore.WHITE)
            else:
                self.p1.is_spiked[1] += 5

        # overheat p1
        if self.p1.is_overheated[0]:
            if self.p1.is_overheated[1] <= 0:
                self.p1.change_health(-15)
                self.p1.is_overheated = [False, 0]
                print(Fore.YELLOW + "P1 found a coolant! P1 is no longer Overheating" + Fore.WHITE)
            else:
                self.p1.change_health(-(self.p1.is_overheated[1] * 5))
                print(Fore.YELLOW + "P1 is Overheating. P1 " + str(
                    -self.p1.is_overheated[1] * 5) + " Health" + Fore.WHITE)
                self.p1.is_overheated[1] -= 1

        # spikes p2
        if self.p2.is_spiked[0]:
            self.p2.change_speed(-self.p2.is_spiked[1])
            print(Fore.YELLOW + "P2 is affected by Spikes. P2 " + str(-self.p2.is_spiked[1]) + " Speed" + Fore.WHITE)
            if self.p2.is_spiked[1] >= 20:
                self.p2.is_spiked = [False, 0]
                print(Fore.YELLOW + "P2 found a spare tire! P2 is no longer affected by Spikes" + Fore.WHITE)
            else:
                self.p2.is_spiked[1] += 5

        # overheat p2
        if self.p2.is_overheated[0]:
            if self.p2.is_overheated[1] <= 0:
                self.p2.is_overheated = [False, 0]
                print(Fore.YELLOW + "P2 found a coolant! P2 is no longer Overheating" + Fore.WHITE)
            else:
                self.p2.change_health(-(self.p2.is_overheated[1] * 5))
                print(Fore.YELLOW + "P2 is Overheating. P2 " + str(
                    -self.p2.is_overheated[1] * 5) + " Health" + Fore.WHITE)
                self.p2.is_overheated[1] -= 1
                
        if self.p1.health <= 0:
            self.p1.sprite = 'DED'
        if self.p2.health <= 0:
            self.p2.sprite = 'DED'

    def print_progress(self, turn, include_status: bool = True) -> None:
        print(Fore.BLUE + "P1: " + (30 - self.p1.progress) * '_' + self.p1.sprite + (self.p1.progress * '_'))
        print(Fore.RED + "P2: " + (30 - self.p2.progress) * '_' + self.p2.sprite + (self.p2.progress * '_'))

        print(Fore.BLUE + "P1: Health = " + str(self.p1.health) + ", Speed = " + str(self.p1.speed))
        print(Fore.RED + "P2: Health = " + str(self.p2.health) + ", Speed = " + str(self.p2.speed))

        if self.has_p1_won():
            print(Fore.BLUE + "P1 WON!")
        if self.has_p2_won():
            print(Fore.RED + "P2 WON!")
        
        if include_status:
            if turn % 2 == 0:
                print(Fore.LIGHTGREEN_EX + "P1 Statuses:", end="")
                if self.p1.is_overheated[0]:
                    print(" Overheated", end="")
                if self.p1.is_spiked[0]:
                    print(" Spiked", end="")
                elif not (self.p1.is_overheated[0] or self.p1.is_spiked[0]):
                    print(" None", end="")
                print(Fore.WHITE)
            else:
                print(Fore.LIGHTGREEN_EX + "P2 Statuses:", end="")
                if self.p2.is_overheated[0]:
                    print(" Overheated", end="")
                if self.p2.is_spiked[0]:
                    print(" Spiked", end="")
                elif not (self.p2.is_overheated[0] or self.p2.is_spiked[0]):
                    print(" None", end="")
                print(Fore.WHITE)

    def clear(self, turn) -> None:
        input(('P1' if turn % 2 == 0 else 'P2') + ', have you finished? (Press Enter)')
        os.system('cls')
        input(('P1' if (turn + 1) % 2 == 0 else 'P2') + ', are you ready? (Press Enter)')

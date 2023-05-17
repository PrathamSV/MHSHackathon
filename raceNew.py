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
        self.is_protected = False

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
            self.sprite = 'DEAD'
        return self.progress

    # spike and overheat don't stack w/ themselves
    def spike(self) -> None:
        self.is_spiked = [True, 10]

    def overheat(self) -> None:
        self.is_overheated = [True, 3]


class Race:
    def v8(self, player: int, is_power: bool) -> None:
        value = 30 if is_power else 20
        if player == 1:
            self.p1.change_speed(value)
        elif player == 2:
            self.p2.change_speed(value)
        print(Fore.YELLOW + f"+{str(value)} Speed." + Fore.WHITE)

    def chassis(self, player: int, is_power: bool) -> None:
        value = 40 if is_power else 30
        neg_value = -15 if is_power else -10
        if player == 1:
            self.p1.change_speed(value)
            self.p1.change_health(neg_value)
        elif player == 2:
            self.p2.change_speed(value)
            self.p2.change_health(neg_value)
        print(Fore.YELLOW + f"+{str(value)} Speed, {str(neg_value)} Health." + Fore.WHITE)

    def fix(self, player: int, is_power: bool) -> None:

        if player == 1:
            if is_power:
                self.p1.is_protected = True
            self.p1.is_spiked = [False, 0]
            self.p1.is_overheated = [False, 0]
        elif player == 2:
            if is_power:
                self.p2.is_protected = True
            self.p2.is_spiked = [False, 0]
            self.p2.is_overheated = [False, 0]
        print(Fore.YELLOW + "All DoT effects removed." + (" And protected next turn." if is_power else "") + Fore.WHITE)

    def repair(self, player: int, is_power: bool) -> None:
        value = 30 if is_power else 20
        if player == 1:
            self.p1.change_health(value)
        elif player == 2:
            self.p2.change_health(value)
        print(Fore.YELLOW + f"+{str(value)} Health." + Fore.WHITE)

    def spikes(self, player: int, is_power: bool) -> None:
        if player == 1:
            if self.p2.is_protected:
                print(Fore.YELLOW + "P2 was Protected! No Damage done" + Fore.WHITE)
                return
            self.p2.spike()
            if is_power:
                self.p2.change_speed(-5)
        elif player == 2:
            if self.p1.is_protected:
                print(Fore.YELLOW + "P1 was Protected! No Damage done" + Fore.WHITE)
                return
            self.p1.spike()
            if is_power:
                self.p1.change_speed(-5)

        print(Fore.YELLOW + "Your opponent was spiked." + (
            " It hit extra hard! Opponent -5 Speed" if is_power else "") + Fore.WHITE)

    def weight(self, player: int, is_power: bool) -> None:
        value = -30 if is_power else -20
        if player == 1:
            if self.p2.is_protected:
                print(Fore.YELLOW + "P2 was Protected! No Damage done" + Fore.WHITE)
                return
            self.p2.change_speed(value)
        elif player == 2:
            if self.p1.is_protected:
                print(Fore.YELLOW + "P1 was Protected! No Damage done" + Fore.WHITE)
                return
            self.p1.change_speed(value)
        print(Fore.YELLOW + f"Opponent {str(value)} Speed." + Fore.WHITE)

    def explosive(self, player: int, is_power: bool) -> None:
        value = -40 if is_power else -30
        neg_value = -15 if is_power else -10
        did_self_dmg = False
        if player == 1:
            if self.p2.is_protected:
                print(Fore.YELLOW + "P2 was Protected! No Damage done" + Fore.WHITE)
                return
            self.p2.change_health(value)
            if random.choice([True, False]):
                self.p1.change_health(neg_value)
                did_self_dmg = True
        elif player == 2:
            if self.p1.is_protected:
                print(Fore.YELLOW + "P1 was Protected! No Damage done" + Fore.WHITE)
                return
            self.p1.change_health(value)
            if random.choice([True, False]):
                self.p2.change_health(neg_value)
                did_self_dmg = True

        if did_self_dmg:
            out = f"Opponent {str(value)} Health. But you damaged yourself in the process. Self {str(neg_value)} Health."
        else:
            out = f"Opponent {str(value)} Health."

        print(Fore.YELLOW + out + Fore.WHITE)

    def overheat(self, player: int, is_power: bool) -> None:
        if player == 1:
            if self.p2.is_protected:
                print(Fore.YELLOW + "P2 was Protected! No Damage done" + Fore.WHITE)
                return
            self.p2.overheat()
            if is_power:
                self.p2.change_health(-5)
        elif player == 2:
            if self.p1.is_protected:
                print(Fore.YELLOW + "P1 was Protected! No Damage done" + Fore.WHITE)
                return
            self.p1.overheat()
            if is_power:
                self.p1.change_health(-5)
        print(Fore.YELLOW + "Opponent has Overheated." + (
            " It hit extra hard! Opponent -5 Health" if is_power else "") + Fore.WHITE)

    def speed_limit(self, player: int, is_power: bool) -> None:
        self_got_caught = False
        opp_got_caught = False
        limit = random.randint(20, 80)
        print(Fore.YELLOW + "The speed limit is " + str(limit) + Fore.WHITE)

        if player == 1:
            if self.p2.is_protected:
                print(Fore.YELLOW + "P2 was Protected! No Damage done" + Fore.WHITE)
                return
            if self.p2.speed >= limit:
                self.p2.change_speed(-30)
                opp_got_caught = True
            if self.p1.speed >= limit and random.choice([True, False]):
                if not is_power:
                    self.p1.change_speed(-10)
                    self_got_caught = True
        elif player == 2:
            if self.p1.is_protected:
                print(Fore.YELLOW + "P1 was Protected! No Damage done" + Fore.WHITE)
                return
            if self.p1.speed >= limit:
                self.p1.change_speed(-30)
                opp_got_caught = True
            if self.p2.speed >= limit and random.choice([True, False]):
                if not is_power:
                    self.p2.change_speed(-10)
                    self_got_caught = True

        out = ""
        if opp_got_caught:
            out += "Your opponent was over the Speed Limit! Opp -30 Speed."
        if self_got_caught:
            out += "You were above the Speed Limit! Self -10 Speed."

        print(Fore.YELLOW + out + Fore.WHITE)

    def nothing(self, _: int, __: bool):  # do nothing
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

    def update_progress(self, turn: int, card: int, is_power: bool) -> None:
        if turn % 2 == 1:
            if self.p1.is_protected:
                self.p1.is_protected = False
            # call card
            self.call_dict[card](1, is_power)
            # update
            self.p1.update_progress()
        if turn % 2 == 0:
            if self.p2.is_protected:
                self.p2.is_protected = False
            # call card
            self.call_dict[card](2, is_power)
            # update
            self.p2.update_progress()

        if self.p1.is_protected:
            print(Fore.YELLOW + "P1 is protected, no existing DoT will be applied." + Fore.WHITE)
        else:
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

        if self.p2.is_protected:
            print(Fore.YELLOW + "P2 is protected, no existing DoT will be applied." + Fore.WHITE)
        else:
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
            self.p1.sprite = 'DEAD'
        if self.p2.health <= 0:
            self.p2.sprite = 'DEAD' 

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

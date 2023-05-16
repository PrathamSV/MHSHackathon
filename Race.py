class Car:
    def __init__(self, speed=10, health=100):
        self.speed = speed
        self.health = health
        self.progress = 0
        self.sprite = 'CAR'

    def change_health(self, amount):
        self.health += self.health * (amount / 100)

    def change_speed(self, amount):
        self.speed += self.speed * (amount / 100)

    def update_progress(self):
        self.progress += int(self.speed / 10)
        if self.health <= 0:
            self.sprite = 'DED'
        return self.progress


from colorama import Fore


class Race:
    def __init__(self, p1: Car, p2: Car):
        self.p1 = p1
        self.p2 = p2

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

    def update_progress(self, player, card=1):
        if player == 1:
            self.p1.update_progress()
        if player == 2:
            self.p2.update_progress()

    def print_progress(self):
        print(Fore.BLUE + "P1: " + (30 - p1.progress) * '_' + p1.sprite + (p1.progress * '_'))
        print(Fore.RED + "P2: " + (30 - p2.progress) * '_' + p2.sprite + (p2.progress * '_'))
        if self.has_p1_won():
            print(Fore.BLUE + "P1 WON!")
        if self.has_p2_won():
            print(Fore.RED + "P2 WON!")

        print(Fore.WHITE, end='')

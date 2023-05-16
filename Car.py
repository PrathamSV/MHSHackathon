class Car:
    def __init__(self, speed, health):
        self.speed = speed
        self.health = health

    def change_health(self, amount):
        self.health += amount

    def change_speed(self, amount):
        self.speed += amount

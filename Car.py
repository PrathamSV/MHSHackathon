class Car:
    def __init__(self, speed=50, health=100):
        self.speed = speed
        self.health = health

    def change_health(self, amount):
        self.health += self.health * (amount/100)

    def change_speed(self, amount):
        self.speed += self.speed * (amount/100)

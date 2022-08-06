from src.server import User

INITIAL_MONEY = 10_000
INITIAL_WORKSHOPS = 2
INITIAL_ORE = 4
INITIAL_AIRSHIPS = 2

STORE_ORE_COST = 300
STORE_AIRSHIP_COST = 500
STORE_WORKSHOP_COST = 1_000


class Player:
    def __init__(self, user: User):
        self.user = user
        self.money = INITIAL_MONEY
        self.workshops = INITIAL_WORKSHOPS
        self.ore = INITIAL_ORE
        self.airships = INITIAL_AIRSHIPS
        self.dead = False

    def event_store_ore(self):
        self.money -= self.ore * STORE_ORE_COST

    def event_store_airships(self):
        self.money -= self.airships * STORE_AIRSHIP_COST

    def event_store_workshops(self):
        self.money -= self.workshops * STORE_WORKSHOP_COST

    def trigger_ore_request(self, amount: int, price: int):
        self.money -= amount * price
        self.ore += amount

    def trigger_sell_request(self, amount: int, price: int):
        self.money += amount * price
        self.airships -= amount

    def trigger_workshop_build(self):
        self.workshops += 1

    def dictify(self):
        return {
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'avatar': self.user.avatar
            },
            'money': self.money,
            'workshops': self.workshops,
            'ore': self.ore,
            'airships': self.airships,
            'dead': self.dead
        }

    def __repr__(self):
        return f'{not self.dead}Player(user={self.user}, money={self.money}, workshops={self.workshops}, ore={self.ore}, airships={self.airships})'

from random import choices

INITIAL_LEVEL = 3

LEVELS = {
    1: {
        'total_ore': lambda p: int(1.0 * p),
        'airships_demand': lambda p: int(3.0 * p),
        'minimal_price': 800,
        'maximal_price': 6_500,
        'chances': {
            1: 1 / 3,
            2: 1 / 3,
            3: 1 / 6,
            4: 1 / 12,
            5: 1 / 12
        },
    },
    2: {
        'total_ore': lambda p: int(1.5 * p),
        'airships_demand': lambda p: int(2.5 * p),
        'minimal_price': 650,
        'maximal_price': 6_000,
        'chances': {
            1: 1 / 4,
            2: 1 / 3,
            3: 1 / 4,
            4: 1 / 12,
            5: 1 / 12
        },
    },
    3: {
        'total_ore': lambda p: int(2.0 * p),
        'airships_demand': lambda p: int(2.0 * p),
        'minimal_price': 500,
        'maximal_price': 5_500,
        'chances': {
            1: 1 / 12,
            2: 1 / 4,
            3: 1 / 3,
            4: 1 / 4,
            5: 1 / 12
        },
    },
    4: {
        'total_ore': lambda p: int(2.5 * p),
        'airships_demand': lambda p: int(1.5 * p),
        'minimal_price': 400,
        'maximal_price': 5_000,
        'chances': {
            1: 1 / 12,
            2: 1 / 12,
            3: 1 / 4,
            4: 1 / 3,
            5: 1 / 4
        },
    },
    5: {
        'total_ore': lambda p: int(3.0 * p),
        'airships_demand': lambda p: int(1.0 * p),
        'minimal_price': 300,
        'maximal_price': 4_500,
        'chances': {
            1: 1 / 12,
            2: 1 / 12,
            3: 1 / 6,
            4: 1 / 3,
            5: 1 / 3
        },
    },
}


class MarketState:
    def __init__(self):
        self.level = INITIAL_LEVEL
        self.state = LEVELS[self.level]

    def set_random_state(self):
        self.level = choices(
            list(LEVELS[self.level]['chances'].keys()),
            list(LEVELS[self.level]['chances'].values())
        )[0]
        self.state = LEVELS[self.level]

    def dictify(self, p):
        return {
            'level': self.level,
            'total_ore': self.state['total_ore'](p),
            'airships_demand': self.state['airships_demand'](p),
            'minimal_price': self.state['minimal_price'],
            'maximal_price': self.state['maximal_price'],
        }

    def __str__(self):
        return f'MarketState (level={self.level}, state={self.state})'

import logging
import pickle
import random
import uuid
import warnings

import numpy as np
from sklearn.multioutput import MultiOutputRegressor

from src import Player, Session
from src.game.Player import STORE_WORKSHOP_COST
from src.server import User

with open('./model.ai', 'rb') as f:
    MODEL: MultiOutputRegressor = pickle.load(f)

AI_AVATAR = 'https://avatarfiles.alphacoders.com/307/307892.png'

logger = logging.getLogger('ai')
logger.setLevel(logging.DEBUG)


def normalize_price(price: float):
    price += random.choice([-150, -100, -50, 0, 50, 100, 150])
    return round(price * 2, -2) // 2


class AI(Player):
    def __init__(self):
        bot_id = uuid.uuid4().hex[:8]
        super().__init__(User(id=bot_id, name=f'AI ({bot_id})', password='', avatar=AI_AVATAR, wins=69, looses=1338))

    def get_move(self, session: Session):
        total_ore = session.market_state.state['total_ore'](session.p)
        airships_demand = session.market_state.state['airships_demand'](session.p)
        minimal_price = session.market_state.state['minimal_price']
        maximal_price = session.market_state.state['maximal_price']

        x = {
            'money': self.money,
            'workshops': self.workshops,
            'ore': self.ore,
            'airships': self.airships,
            'market_level': session.market_state.level,
            'market_total_ore': total_ore,
            'market_airships_demand': airships_demand,
            'market_minimal_price': minimal_price,
            'market_maximal_price': maximal_price
        }
        x_df = np.array([list(x.values())])
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            predicted = MODEL.predict(x_df)[0]

        move = {
            'ore_request_amount': predicted[0],
            'ore_request_price': predicted[1],
            'airships_amount': predicted[2],
            'sell_request_amount': predicted[3],
            'sell_request_price': predicted[4],
            'build_workshop': predicted[5]
        }

        logger.info(f'AI {self.user.id} generated: {move}')

        # normalization
        move['user'] = self.user
        move['ore_request_amount'] = round(move['ore_request_amount'])
        move['ore_request_price'] = normalize_price(move['ore_request_price'])
        move['airships_amount'] = round(move['airships_amount'])
        move['sell_request_amount'] = round(move['sell_request_amount'])
        move['sell_request_price'] = normalize_price(move['sell_request_price'])
        move['build_workshop'] = move['build_workshop'] > 0.5

        # impossible moves fixes
        if move['ore_request_amount'] > total_ore:
            move['ore_request_amount'] = total_ore

        if move['ore_request_price'] < minimal_price:
            move['ore_request_price'] = minimal_price

        if move['airships_amount'] > airships_demand:
            move['airships_amount'] = airships_demand

        if move['sell_request_amount'] > self.airships:
            move['sell_request_amount'] = self.airships

        if move['sell_request_price'] > maximal_price:
            move['sell_request_price'] = maximal_price

        if move['build_workshop'] and self.money <= STORE_WORKSHOP_COST:
            move['build_workshop'] = False

        logger.info(f'AI {self.user.id} normalized: {move}')

        # dummy moves fixes

        # too many ores or not enough money
        if self.ore > 6 or self.money <= 8000:
            move['ore_request_amount'] = 0

        # too many airships or not enough money
        if self.airships > 6 or self.money <= 8000:
            move['airships_amount'] = 0

        # well...
        if self.workshops > 5:
            move['build_workshop'] = False

        # too low sell price
        if move['sell_request_price'] < maximal_price * 0.8:
            move['sell_request_price'] = normalize_price(maximal_price * 0.85)

        # just to make sure AI will stay alive if it has airships
        if self.money <= 6000 and self.airships > 0:
            move['sell_request_amount'] = self.airships
            move['sell_request_price'] = maximal_price - 700

        # do not build if not enough money
        if self.money <= 6000 and move['airships_amount'] > 0:
            move['airships_amount'] = 0

        logger.info(f'AI {self.user.id} fixed: {move}')

        return move

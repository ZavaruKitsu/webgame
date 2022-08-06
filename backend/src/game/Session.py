import logging
import random
from typing import List, Tuple

from src.game.requests import *
from src.server import User
from .GameException import GameException
from .MarketState import MarketState
from .Player import Player

AIRSHIP_COST = 2_000
WORKSHOP_COST = 5_000

logger = logging.getLogger('session')
logger.setLevel(logging.DEBUG)


class Session:
    def __init__(self, session_id: str, players: List[Player], months: int):
        self.session_id: str = session_id
        self.months = months

        self.ended = False
        self.finalized = False

        self.players: List[Player] = players
        self.queue: List[Player] = list(players)
        random.shuffle(self.queue)

        from .AI import AI
        while isinstance(self.queue[0], AI):
            random.shuffle(self.queue)

        self.initial_player = self.queue[0]

        self.month: int = 1

        self.ore_requests: List[OreRequest] = []
        self.airship_requests: List[AirshipRequest] = []
        self.sell_requests: List[AirshipsSellRequest] = []
        self.workshop_requests: List[Tuple[WorkshopBuildRequest, int]] = []

        self.market_state: MarketState = MarketState()

        self.messages_queue = []

        logger.info(f'Initialized Session with ID: {self.session_id}')

    def get_alive_players(self):
        return list(filter(lambda x: not x.dead, self.players))

    def get_player(self, user: User):
        for item in self.players:
            if item.user.id == user.id:
                return item

    def remove_player(self, user: User):
        player = self.get_player(user)

        self.queue.remove(player)
        self.players.remove(player)

        if not self.players:
            return

        if player == self.initial_player:
            self.initial_player = self.queue[0]

        preds = [req for req in self.ore_requests if req.user.id == user.id]
        for r in preds:
            self.ore_requests.remove(r)

        preds = [req for req in self.airship_requests if req.user.id == user.id]
        for r in preds:
            self.airship_requests.remove(r)

        preds = [req for req in self.sell_requests if req.user.id == user.id]
        for r in preds:
            self.sell_requests.remove(r)

        preds = [req for req in self.workshop_requests if req[0].user.id == user.id]
        for r in preds:
            self.workshop_requests.remove(r)

    @property
    def p(self):
        return len(self.get_alive_players())

    @property
    def only_bots_alive(self):
        from .AI import AI
        return all(isinstance(user, AI) for user in self.get_alive_players())

    def trigger_next_month(self):
        logger.info('Next month triggered')

        # EVENT 1
        # ore requests
        self.trigger_ore_requests()

        # EVENT 2
        # sell requests
        self.trigger_airships_sell()

        # EVENT 3
        # expenses paying
        for player in self.get_alive_players():
            player.event_store_ore()
            player.event_store_airships()
            player.event_store_workshops()

        # EVENT 4
        # market state determining
        level = self.market_state.level
        self.market_state.set_random_state()

        if level != self.market_state.level:
            logger.info(f'New market state: {self.market_state}')
            self.messages_queue.append(f'Новый уровень рынка: {level} → {self.market_state.level}')

        # EVENT 5
        # build airships
        self.trigger_airships_build()

        # EVENT 6
        # build workshops
        self.trigger_workshops_build()

        self.month += 1

        # and finally kill players with money < 0
        self.kill_players()

        if not self.ended:
            self.messages_queue.append('Следующий месяц!')

    def kill_players(self):
        for player in self.players:
            if not player.dead and player.money < 0:
                player.dead = True
                self.queue.remove(player)

                self.messages_queue.append(f'Игрок {player.user.name} обанкротился!')

                logger.info(f'{player} is dead now')

        if self.p == 1 or self.p == 0 or self.month == self.months + 1 or self.only_bots_alive or self.ended:
            self.ended = True

            if not self.finalized:
                if self.p > 0:
                    self.messages_queue.append(f'Игра окончена на {self.month} месяце! Выиграл(-и): ' + ', '.join(
                        player.user.name for player in self.get_alive_players()))
                else:
                    self.messages_queue.append(f'Игра окончена на {self.month} месяце! Все обанкротились.')

                self.finalized = True

    def trigger_move(self, user: User, ore_request_amount: int, ore_request_price: int, airships_amount: int,
                     sell_request_amount: int, sell_request_price: int, build_workshop: bool):
        player = self.get_player(user)

        if user.id != self.queue[0].user.id:
            raise GameException()

        if not player.dead:
            try:
                self.event_request_ore(user, ore_request_amount, ore_request_price)
            except GameException:
                logger.error('Failed to request ore')

            try:
                self.event_request_airship_build(user, airships_amount)
            except GameException:
                logger.error('Failed to request airships building')

            try:
                self.event_request_sell(user, sell_request_amount, sell_request_price)
            except GameException:
                logger.error('Failed to request sell')

            if build_workshop:
                try:
                    self.event_request_workshop_build(user)
                except GameException:
                    logger.error('Failed to request workshop building')

        self.queue.append(self.queue.pop(0))
        while 1:
            if self.queue[0].user.id == user.id:  # all players died
                self.ended = True

                break
            elif self.queue[0].dead:
                self.queue.append(self.queue.pop(0))
            else:
                break

        self.kill_players()

        if self.ended:
            return

        if self.initial_player.user.id == self.queue[0].user.id:
            self.trigger_next_month()

        if not self.queue:
            self.ended = True
            self.kill_players()
            return

        # hack for the PyCharm hints...
        from .AI import AI

        possible_ai = self.queue[0]
        if isinstance(possible_ai, AI):
            ai_move = possible_ai.get_move(self)
            self.trigger_move(**ai_move)

    def trigger_workshops_build(self):
        done = []

        for i, (request, month) in enumerate(self.workshop_requests):
            if month == 4:
                player = self.get_player(request.user)
                player.trigger_workshop_build()

                done.append((request, month))

                logger.info(f'Built workshop for {request.user}')
            else:
                self.workshop_requests[i] = (request, month + 1)

                logger.info(f'Increase workshop month for {request.user}')

        for item in done:
            self.workshop_requests.remove(item)

    def trigger_airships_build(self):
        for request in self.airship_requests:
            player = self.get_player(request.user)
            player.airships += request.amount

            logger.info(f'Built {request.amount} airships for {player}')

        self.airship_requests.clear()

    def trigger_ore_requests(self):
        logger.info('Ore requests triggered')
        amount = self.market_state.state['total_ore'](self.p)
        logger.info(f'Available ore: {amount}')

        while amount > 0 and self.ore_requests:
            highest = max(self.ore_requests, key=lambda r: r.price)
            predicates = [request for request in self.ore_requests if request.price == highest.price]
            logger.info(f'Highest: {highest}, predicates: {predicates}')

            for request in predicates:
                if amount <= 0:
                    break

                # if bank has fewer amount
                if amount - request.amount < 0:
                    satisfied = amount
                else:
                    satisfied = request.amount

                amount -= satisfied
                if satisfied > 0:
                    self.messages_queue.append(
                        f'Банк продал руду {request.user.name} ({satisfied}/{request.amount}) за {request.price * satisfied} ₽')

                player = self.get_player(request.user)
                player.trigger_ore_request(satisfied, request.price)

                logger.info(f'Satisfied {satisfied} for {player} with price {request.price}')

                self.ore_requests.remove(request)

        logger.info(f'Remaining: {amount}')

        self.ore_requests.clear()

    def trigger_airships_sell(self):
        logger.info('Airships sell triggered')
        amount = self.market_state.state['airships_demand'](self.p)
        logger.info(f'Can buy: {amount}')

        while amount > 0 and self.sell_requests:
            lowest = min(self.sell_requests, key=lambda r: r.price)
            predicates = [request for request in self.sell_requests if request.price == lowest.price]
            logger.info(f'Lowest: {lowest}, predicates: {predicates}')

            for request in predicates:
                if amount <= 0:
                    break

                # if bank has fewer amount
                if amount - request.amount < 0:
                    satisfied = amount
                else:
                    satisfied = request.amount

                amount -= satisfied
                if satisfied > 0:
                    self.messages_queue.append(
                        f'Банк купил у {request.user.name} {satisfied}/{request.amount} самолёт(-ов) на сумму {request.price * satisfied} ₽')

                player = self.get_player(request.user)
                player.trigger_sell_request(satisfied, request.price)

                logger.info(f'Satisfied {satisfied} for {player} with price {request.price}')

                self.sell_requests.remove(request)

        logger.info(f'Remaining: {amount}')

        self.sell_requests.clear()

    def event_request_ore(self, user: User, amount: int, price: int):
        if not (self.market_state.state['minimal_price'] <= price) or not (
                0 < amount <= self.market_state.state['total_ore'](self.p)):
            raise GameException()

        request = OreRequest(user, amount, price)
        self.ore_requests.append(request)

        logger.info(f'event_request_ore: {request}')

    def event_request_airship_build(self, user: User, amount: int):
        player = self.get_player(user)

        total_cost = amount * AIRSHIP_COST
        total_ore = amount

        if amount <= 0 or total_ore > player.ore or total_cost > player.money:
            raise GameException()

        player.money -= total_cost
        player.ore -= amount

        request = AirshipRequest(user, amount)
        self.airship_requests.append(request)

        logger.info(f'event_request_airship_build: {request}')

    def event_request_sell(self, user: User, amount: int, price: int):
        player = self.get_player(user)

        if player.airships < amount or amount == 0 or price <= 0:
            raise GameException()

        request = AirshipsSellRequest(user, amount, price)
        self.sell_requests.append(request)

        logger.info(f'event_request_sell: {request}')

    def event_request_workshop_build(self, user: User):
        player = self.get_player(user)

        if player.money < WORKSHOP_COST:
            raise GameException()

        player.money -= WORKSHOP_COST

        request = WorkshopBuildRequest(user)
        self.workshop_requests.append((request, 0))

        logger.info(f'event_request_workshop_build: {request}')

    def dictify(self):
        return {
            'id': self.session_id,
            'players': [player.dictify() for player in self.players],
            'month': self.month,
            'months': self.months,
            'market_state': self.market_state.dictify(self.p),
            'queue': [player.user.id for player in self.queue],
            'ended': self.ended
        }

    def __str__(self):
        return f'Session (session_id={self.session_id}, month={self.month}, market_state={self.market_state}, players={self.players})'

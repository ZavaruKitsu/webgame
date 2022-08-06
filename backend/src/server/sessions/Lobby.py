from typing import List

from src.game.AI import AI
from src.game.Player import Player
from src.game.Session import Session
from src.server.Database import User
from src.server.sessions.LobbyUser import LobbyUser


class Lobby:
    def __init__(self, lobby_id: str, months: int, bots: int):
        self.lobby_id = lobby_id
        self.months = months
        self.bots = bots

        self.users: List[LobbyUser] = []

    def add_user(self, user: User) -> LobbyUser:
        lobby_user = LobbyUser(user)
        self.users.append(lobby_user)

        return lobby_user

    def remove_user(self, user: User):
        for item in self.users:
            if item.user.id == user.id:
                self.users.remove(item)
                break

    def user_ready_switch(self, user: User):
        for item in self.users:
            if item.user.id == user.id:
                item.ready = not item.ready

    def create_session(self):
        players = [Player(item.user) for item in self.users]
        for _ in range(self.bots):
            players.append(AI())

        session = Session(self.lobby_id, players, self.months)

        return session

    @property
    def all_ready(self):
        return all(user.ready for user in self.users)

    def dictify(self):
        return {
            'id': self.lobby_id,
            'users': [user.dictify() for user in self.users]
        }

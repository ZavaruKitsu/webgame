import logging
import uuid
from typing import Tuple, Dict

from src.server.Database import User
from src.server.sessions.Lobby import Lobby
from src.server.sessions.LobbyUser import LobbyUser

logger = logging.getLogger('lobby_hub')
logger.setLevel(logging.DEBUG)


class LobbyHub:
    def __init__(self):
        self.lobbies: Dict[str, Lobby] = {}
        self.users: Dict[str, Lobby] = {}

    def create_lobby(self, creator: User, months: int, bots: int) -> Tuple[Lobby, LobbyUser]:
        lobby_id = uuid.uuid4().hex[:8]
        lobby = Lobby(lobby_id, months, bots)

        self.lobbies[lobby_id] = lobby
        _, lobby_user = self.add_user(lobby_id, creator)

        return lobby, lobby_user

    def has_lobby(self, user: User) -> bool:
        return user.id in self.users

    def remove_lobby(self, lobby: Lobby):
        del self.lobbies[lobby.lobby_id]

        to_remove = []
        for k, v in self.users.items():
            if v.lobby_id == lobby.lobby_id:
                to_remove.append(k)

        for item in to_remove:
            del self.users[item]

        logger.info(f'Removed {lobby.lobby_id}')

    def lobby_exists(self, lobby_id: str) -> bool:
        return lobby_id in self.lobbies

    def add_user(self, lobby_id: str, user: User) -> Tuple[Lobby, LobbyUser]:
        lobby = self.lobbies[lobby_id]
        lobby_user = lobby.add_user(user)

        self.users[user.id] = lobby

        return lobby, lobby_user

    def remove_user(self, user: User) -> Lobby:
        lobby = self.users.pop(user.id)
        lobby.remove_user(user)

        return lobby

    def get_lobby_by_user(self, user: User) -> Lobby:
        return self.users[user.id]

    def get_lobby_by_id(self, lobby_id: str) -> Lobby:
        return self.lobbies[lobby_id]
